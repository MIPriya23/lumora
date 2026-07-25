"""
Gemini Service wrapper for RecoveryAI.
Handles API communication, multimodal audio processing, and structured JSON parsing.
"""

import os
import json
import re
import importlib
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from prompts import (
    SYSTEM_SAFETY_INSTRUCTIONS,
    CHECKIN_SYSTEM_PROMPT,
    CHECKIN_USER_PROMPT,
    EMERGENCY_SYSTEM_PROMPT,
    EMERGENCY_USER_PROMPT,
    SAFETY_PLAN_SYSTEM_PROMPT,
    SAFETY_PLAN_USER_PROMPT,
    EDUCATION_SYSTEM_PROMPT,
    EDUCATION_USER_PROMPT
)

# Optional SDK Imports at top level
try:
    from google import genai
    from google.genai import types
    HAS_GENAI_SDK = True
except ImportError:
    genai = None  # type: ignore
    types = None  # type: ignore
    HAS_GENAI_SDK = False

try:
    genai_legacy = importlib.import_module("google.generativeai")
    HAS_LEGACY_SDK = True
except ImportError:
    genai_legacy = None
    HAS_LEGACY_SDK = False


class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        self.use_legacy_sdk = False
        self._initialize_client()

    def _initialize_client(self):
        """Try initializing google-genai SDK first, fall back to google-generativeai if needed."""
        # Always reload env to catch updated key (check .env then .env.example)
        load_dotenv(override=True)
        if not os.getenv("GEMINI_API_KEY"):
            load_dotenv(".env.example", override=True)
        self.api_key = self.api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            self.client = None
            return

        if HAS_GENAI_SDK and genai is not None:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self.use_legacy_sdk = False
                return
            except Exception as e:
                print(f"Error initializing google-genai client: {e}")

        if HAS_LEGACY_SDK and genai_legacy is not None:
            try:
                genai_legacy.configure(api_key=self.api_key)
                self.client = genai_legacy
                self.use_legacy_sdk = True
                return
            except Exception as e:
                print(f"Error initializing legacy Gemini SDK: {e}")

        self.client = None

    def is_configured(self) -> bool:
        """Check if Gemini API Key is set and client is ready. Re-initializes if key was added."""
        if self.client is None:
            self._initialize_client()
        return self.client is not None and bool(self.api_key) and self.api_key != "your_gemini_api_key_here"

    def _clean_json_string(self, text: str) -> str:
        """Extract JSON block from model response text if wrapped in markdown code fence or extra text."""
        text = text.strip()
        if "```json" in text:
            match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
            if match:
                return match.group(1).strip()
        elif "```" in text:
            match = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # Fallback: extract substring between first '{' and last '}'
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start:end+1]
            
        return text

    def _call_gemini(self, system_instruction: str, user_prompt: str, mime_type: str = "application/json", audio_data: Optional[bytes] = None, audio_mime: str = "audio/wav") -> str:
        """Helper to invoke Gemini API with system instructions and JSON requirement."""
        if not self.is_configured():
            raise ValueError("GEMINI_API_KEY is not set or invalid. Please check your .env file.")

        full_system = f"{SYSTEM_SAFETY_INSTRUCTIONS}\n\n{system_instruction}"

        # Candidate models in order of priority (utilize alias endpoints for maximum availability)
        candidate_models = ["gemini-flash-latest", "gemini-flash-lite-latest", "gemini-2.0-flash", "gemini-2.5-flash"]
        last_exception = None

        if not self.use_legacy_sdk and types is not None:
            # Using official google-genai SDK
            contents = []
            if audio_data:
                contents.append(
                    types.Part.from_bytes(
                        data=audio_data,
                        mime_type=audio_mime
                    )
                )
            contents.append(user_prompt)

            config = types.GenerateContentConfig(
                system_instruction=full_system,
                temperature=0.3,
                response_mime_type="application/json"
            )
            
            for model_name in candidate_models:
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=config
                    )
                    if response and response.text:
                        return response.text
                except Exception as e:
                    last_exception = e
                    continue
            
            raise RuntimeError(f"Gemini API Call Failed across all models: {str(last_exception)}")

        elif HAS_LEGACY_SDK and genai_legacy is not None:
            # Using legacy google.generativeai SDK fallback
            for model_name in candidate_models:
                try:
                    model = genai_legacy.GenerativeModel(
                        model_name=model_name,
                        system_instruction=full_system,
                        generation_config={"response_mime_type": "application/json", "temperature": 0.3}
                    )
                    if audio_data:
                        parts = [{'mime_type': audio_mime, 'data': audio_data}, user_prompt]
                        response = model.generate_content(parts)
                    else:
                        response = model.generate_content(user_prompt)
                    if response and response.text:
                        return response.text
                except Exception as e:
                    last_exception = e
                    continue

            raise RuntimeError(f"Gemini API Call Failed across legacy models: {str(last_exception)}")

        else:
            raise RuntimeError("No compatible Gemini SDK available.")

    def _parse_json_response(self, raw_response: str) -> Dict[str, Any]:
        """Clean and parse JSON from model output with fallback error recovery."""
        cleaned = self._clean_json_string(raw_response)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback 1: strip trailing commas before closing braces/brackets
            sanitized = re.sub(r',\s*([\]}])', r'\1', cleaned)
            try:
                return json.loads(sanitized)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse Gemini response as JSON: {str(e)}\nRaw Response: {raw_response[:200]}")

    def check_in(self, user_input: str, audio_bytes: Optional[bytes] = None, audio_mime: str = "audio/wav") -> Dict[str, Any]:
        """Feature 1: Mental Health Check-In analysis."""
        prompt = CHECKIN_USER_PROMPT.format(user_input=user_input or "Voice check-in provided.")
        raw_response = self._call_gemini(
            system_instruction=CHECKIN_SYSTEM_PROMPT,
            user_prompt=prompt,
            audio_data=audio_bytes,
            audio_mime=audio_mime
        )
        return self._parse_json_response(raw_response)

    def get_emergency_support(self, context: str = "Immediate urge / high distress") -> Dict[str, Any]:
        """Feature 2: Emergency Support Script Generator."""
        prompt = EMERGENCY_USER_PROMPT.format(context=context)
        raw_response = self._call_gemini(
            system_instruction=EMERGENCY_SYSTEM_PROMPT,
            user_prompt=prompt
        )
        return self._parse_json_response(raw_response)

    def generate_safety_plan(self, trigger_input: str) -> Dict[str, Any]:
        """Feature 3: Safety Plan Generator."""
        prompt = SAFETY_PLAN_USER_PROMPT.format(trigger_input=trigger_input)
        raw_response = self._call_gemini(
            system_instruction=SAFETY_PLAN_SYSTEM_PROMPT,
            user_prompt=prompt
        )
        return self._parse_json_response(raw_response)

    def explain_craving(self, query_input: str) -> Dict[str, Any]:
        """Feature 4: Recovery Education."""
        prompt = EDUCATION_USER_PROMPT.format(query_input=query_input)
        raw_response = self._call_gemini(
            system_instruction=EDUCATION_SYSTEM_PROMPT,
            user_prompt=prompt
        )
        return self._parse_json_response(raw_response)
