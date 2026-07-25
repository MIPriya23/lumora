"""
RecoveryAI Test Suite - Comprehensive Unit Tests
"""

import unittest
import json
from unittest.mock import MagicMock, patch

import prompts
import utils
from gemini_service import GeminiService


class TestPrompts(unittest.TestCase):
    """Test safety prompts and template formatting."""

    def test_system_safety_instructions(self):
        self.assertIn("CRITICAL SAFETY RULES", prompts.SYSTEM_SAFETY_INSTRUCTIONS)
        self.assertIn("NEVER diagnose", prompts.SYSTEM_SAFETY_INSTRUCTIONS)
        self.assertIn("NEVER shame", prompts.SYSTEM_SAFETY_INSTRUCTIONS)
        self.assertIn("988", prompts.SYSTEM_SAFETY_INSTRUCTIONS)

    def test_checkin_prompt_formatting(self):
        formatted = prompts.CHECKIN_USER_PROMPT.format(user_input="Feeling stressed")
        self.assertIn("Feeling stressed", formatted)

    def test_emergency_prompt_formatting(self):
        formatted = prompts.EMERGENCY_USER_PROMPT.format(context="Urge spike")
        self.assertIn("Urge spike", formatted)

    def test_safety_plan_prompt_formatting(self):
        formatted = prompts.SAFETY_PLAN_USER_PROMPT.format(trigger_input="Loneliness")
        self.assertIn("Loneliness", formatted)

    def test_education_prompt_formatting(self):
        formatted = prompts.EDUCATION_USER_PROMPT.format(query_input="Explain dopamine")
        self.assertIn("Explain dopamine", formatted)


class TestUtils(unittest.TestCase):
    """Test UI helpers, CSS rendering, and preset collections."""

    def test_crisis_resources(self):
        self.assertIn("988 Lifeline", utils.CRISIS_RESOURCES)
        self.assertIn("SAMHSA Helpline", utils.CRISIS_RESOURCES)
        self.assertEqual(utils.CRISIS_RESOURCES["988 Lifeline"]["number"], "988")

    def test_render_risk_badge(self):
        badge_low = utils.render_risk_badge("Low")
        self.assertIn("risk-low", badge_low)

        badge_med = utils.render_risk_badge("Medium")
        self.assertIn("risk-medium", badge_med)

        badge_high = utils.render_risk_badge("High")
        self.assertIn("risk-high", badge_high)

        badge_crit = utils.render_risk_badge("Critical")
        self.assertIn("risk-critical", badge_crit)

    def test_preset_lists_non_empty(self):
        self.assertGreaterEqual(len(utils.PRESET_MOODS), 4)
        self.assertGreaterEqual(len(utils.PRESET_TRIGGERS), 4)
        self.assertGreaterEqual(len(utils.PRESET_EDU_TOPICS), 4)


class TestGeminiService(unittest.TestCase):
    """Test GeminiService initialization, JSON cleaning, and mocked API responses."""

    def setUp(self):
        self.service = GeminiService(api_key="test_api_key_123")

    def test_clean_json_string_raw(self):
        raw = '{"risk_level": "Low", "emotional_summary": "Calm"}'
        cleaned = self.service._clean_json_string(raw)
        data = json.loads(cleaned)
        self.assertEqual(data["risk_level"], "Low")

    def test_clean_json_string_markdown(self):
        raw = '```json\n{"risk_level": "High", "emotional_summary": "Anxious"}\n```'
        cleaned = self.service._clean_json_string(raw)
        data = json.loads(cleaned)
        self.assertEqual(data["risk_level"], "High")

    def test_clean_json_string_extra_text(self):
        raw = 'Here is your structured output:\n{"risk_level": "Medium"}\nHope this helps!'
        cleaned = self.service._clean_json_string(raw)
        data = json.loads(cleaned)
        self.assertEqual(data["risk_level"], "Medium")

    @patch.object(GeminiService, '_call_gemini')
    def test_check_in(self, mock_call):
        mock_call.return_value = json.dumps({
            "risk_level": "Medium",
            "emotional_summary": "Feeling overwhelmed after a long day.",
            "trigger_detection": "Stress",
            "recommended_actions": ["Drink water", "Deep breathing"],
            "encouragement": "You are doing great.",
            "crisis_alert_needed": False
        })
        res = self.service.check_in("Feeling stressed")
        self.assertEqual(res["risk_level"], "Medium")
        self.assertEqual(res["trigger_detection"], "Stress")
        self.assertEqual(len(res["recommended_actions"]), 2)

    @patch.object(GeminiService, '_call_gemini')
    def test_get_emergency_support(self, mock_call):
        mock_call.return_value = json.dumps({
            "coping_script": "This feeling will pass.",
            "breathing_guide": "Inhale 4s, Hold 7s, Exhale 8s",
            "immediate_actions": ["Step outside"],
            "caregiver_alert_message": "Need help.",
            "crisis_contacts": {"988": "Call 988"}
        })
        res = self.service.get_emergency_support("Urge spike")
        self.assertIn("coping_script", res)
        self.assertIn("breathing_guide", res)

    @patch.object(GeminiService, '_call_gemini')
    def test_generate_safety_plan(self, mock_call):
        mock_call.return_value = json.dumps({
            "trigger_name": "Loneliness",
            "prevention_plan": "Schedule regular check-ins",
            "coping_techniques": ["Call a friend"],
            "things_to_avoid": ["Isolation"],
            "healthy_alternatives": ["Go for a walk"]
        })
        res = self.service.generate_safety_plan("Loneliness")
        self.assertEqual(res["trigger_name"], "Loneliness")
        self.assertIn("coping_techniques", res)

    @patch.object(GeminiService, '_call_gemini')
    def test_explain_craving(self, mock_call):
        mock_call.return_value = json.dumps({
            "topic": "Dopamine reset",
            "why_it_happens": "Brain rewiring process",
            "recovery_tips": ["Stay patient"],
            "positive_encouragement": "Healing takes time."
        })
        res = self.service.explain_craving("Dopamine reset")
        self.assertEqual(res["topic"], "Dopamine reset")
        self.assertIn("why_it_happens", res)


if __name__ == "__main__":
    unittest.main(verbosity=2)
