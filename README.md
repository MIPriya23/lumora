# ♾️ Lumora - GenAI Recovery & Prevention Platform

> **PromptWars Hackathon MVP**  
> A multi-modal, Generative AI-powered Recovery & Prevention Platform designed for individuals navigating substance use disorders and their caregivers during moments of highest cognitive load.

---

## 🌟 Key Features

1. **💬 Zero-Typing Mental Health Check-In**
   - Express feelings via quick-select mood chips, text, or **voice audio recordings**.
   - Gemini API analyzes input and returns **Risk Level** (Low, Medium, High, Critical), Emotional Summary, Identified Triggers, Recommended Micro-Actions, and Empathetic Encouragement.

2. **⚡ 1-Click Emergency Support ("Need Help Now")**
   - Immediate intervention when cognitive load is highest.
   - Generates an emergency coping script to read out loud, an **interactive 4-7-8 breathing animation**, 1-click immediate grounding actions, and a pre-formatted text message template for trusted caregivers.

3. **♾️ Safety Plan Generator**
   - Select or input today's trigger (e.g., *Loneliness*, *Work Stress*, *Peer Pressure*, *Fatigue*).
   - Gemini generates a structured prevention plan, coping techniques, environments/things to avoid, and healthy alternative activities.

4. **📚 Recovery Education ("Explain My Cravings")**
   - Simple, non-judgmental neurobiological explanations of cravings, dopamine resets, and stress responses.
   - Actionable, science-backed recovery tips and positive reinforcement.

5. **🚨 Contextual Safety Guardrails**
   - Trauma-informed system instructions ensuring **no medical diagnoses**, **zero shaming**, and mandatory 24/7 crisis hotline alerts (988 Lifeline, SAMHSA 1-800-662-4357) for high-risk situations.

---

## 🏗️ Folder Structure

```
RecoveryAI/
├── main.py              # Streamlit Web App UI with tabs, zero-typing chips & cards
├── gemini_service.py    # Gemini SDK wrapper with structured JSON parsing & multimodal audio
├── prompts.py           # Reusable prompt templates & strict safety guardrails
├── utils.py             # UI helpers, CSS theme, risk badges & breathing widget
├── requirements.txt     # Python dependencies
├── README.md            # Documentation & setup instructions
└── .env.example         # Environment variables template
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.10+
- A Google Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

### 1. Clone & Set Up Environment

```bash
cd Recovery_ai
cp .env.example .env
```

Edit `.env` and insert your Gemini API Key:
```env
GEMINI_API_KEY=AIzaSyYourActualKeyHere
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run main.py
```

The app will open automatically in your browser at `http://localhost:8501`.

### 4. Run Unit Tests

```bash
python test_app.py
```
Runs 15 automated unit tests verifying safety prompts, Gemini API wrapper, JSON parsers, and UI helpers.

---

## ☁️ Deployment Steps

### Streamlit Community Cloud (Recommended)
1. Push this repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and select your repository and `main.py`.
4. Under **Advanced settings**, add Secrets:
   ```toml
   GEMINI_API_KEY = "AIzaSyYourActualKeyHere"
   ```
5. Click **Deploy!**

---

## 🧭 Problem Statement Alignment

RecoveryAI is built to directly address the PromptWars problem statement — **"A GenAI-powered platform for recovery & prevention that supports individuals during their highest cognitive-load moments."** Every feature maps to an explicit requirement:

| Problem Statement Requirement | RecoveryAI Feature |
|---|---|
| Support individuals with **substance use disorder** | Trauma-informed, non-judgmental prompts across all four flows |
| Reduce **cognitive load** in crisis moments | Zero-typing preset chips, 1-click emergency button, voice input |
| **Multi-modal** input (text, voice, quick-select) | `st.audio_input` for voice check-in + preset mood chips + text |
| **Real-time risk detection** | Gemini-scored risk levels (Low/Medium/High/Critical) with color + shape indicator |
| **Prevention** planning | Safety Plan Generator with trigger-specific coping & healthy alternatives |
| **Recovery education** | "Explain My Cravings" flow — neurobiology in plain language |
| **Safety guardrails** — no diagnosis, no shaming | System prompts explicitly forbid diagnosis and shame; enforced in `prompts.py` |
| **Crisis escalation** | Mandatory 988 / SAMHSA / Crisis Text Line hotlines in every flow + High-risk banner |
| **Caregiver involvement** | Pre-formatted caregiver alert message template in emergency flow |
| **Accessible to distressed users** | WCAG 2.1 AA: keyboard nav, aria-live regions, prefers-reduced-motion, non-color risk indicators |

### 🔒 Security & Privacy Posture
- All LLM-generated content is HTML-escaped (`html.escape`) before rendering to defuse XSS (OWASP A03).
- API key is loaded from `.env` — never committed, never logged.
- No PII is stored client-side; `st.session_state` is per-browser-session only.
- No third-party analytics or trackers.
- Input length is bounded by Streamlit's default text-area limits.

### ♿ Accessibility Highlights
- Semantic landmarks: `<main>`, `<aside>`, `<section role="region">`, skip-nav link.
- ARIA live regions on emergency alerts, help-request confirmation, and game score updates.
- Risk badges use **shape + color** (◐◑●) so colorblind users can distinguish severity (WCAG 1.4.1).
- Full `@media (prefers-reduced-motion)` support disables decorative animations.
- Keyboard-accessible mini-game (Space/Enter to catch the bird).
- Visible 3px `:focus-visible` outline on every interactive element (WCAG 2.4.7).
- Telephone hotlines rendered as proper `tel:` links with descriptive `aria-label`.

### 🧪 Testing
32 automated unit tests cover:
- Prompt safety guardrails (`988`, `NEVER diagnose`, `NEVER shame`)
- All four Gemini service flows with mocked responses
- Edge cases: empty input, malformed JSON, missing optional fields, placeholder API key
- Accessibility helpers: risk badge case-insensitivity, non-color severity indicator, ARIA labels
- Utility invariants: crisis-resource structure, preset list contents

Run with:
```bash
python test_app.py
```

---

## 🎯 2-Minute Hackathon Demonstration Workflow

1. **Zero-Typing Check-In**: Open the **💬 Mental Health Check-In** page, click the chip `"I'm feeling stressed and want to drink"`, click **Run Check-In Analysis**. Observe the real-time Gemini output with risk level, trigger detection, and micro-actions.
2. **Instant Emergency Support**: Click the big **"🚨 NEED HELP NOW"** button in the header. Watch Gemini generate an immediate coping script, step-by-step grounding actions, and an animated 4-7-8 breathing circle.
3. **Safety Plan**: Open the **♾️ Safety Plan Generator** page, select `"Loneliness & Social Isolation"`, click **Generate Safety Plan**. Review structured prevention techniques and healthy alternatives.
4. **Recovery Education**: Open the **📚 Recovery Education** page, click `"Explain My Cravings"`. Demonstrate how Gemini breaks down complex neuroscience into compassionate, simple language.
5. **Stress-Buster Mini-Game**: Open the **🕊️ Stress Buster Game** page for a 60-second mindfulness break that interrupts the craving loop.
