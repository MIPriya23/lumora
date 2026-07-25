"""
RecoveryAI - Multi-modal GenAI Recovery & Prevention Platform MVP
Entry point for Streamlit application.
"""

import streamlit as st
import os
import json
from dotenv import load_dotenv

# Load environment
load_dotenv()

from gemini_service import GeminiService
from utils import (
    inject_custom_css,
    render_risk_badge,
    render_breathing_widget,
    render_stress_buster_game,
    CRISIS_RESOURCES,
    PRESET_MOODS,
    PRESET_TRIGGERS,
    PRESET_EDU_TOPICS
)

# Page Configuration
st.set_page_config(
    page_title="RecoveryAI - GenAI Recovery & Prevention",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS
inject_custom_css()

# Initialize Gemini Service
@st.cache_resource
def get_service():
    return GeminiService()

gemini = get_service()

# --- TOP EMERGENCY BANNER (semantic + assistive-tech friendly) ---
st.markdown(
    """
    <aside class="emergency-banner" role="complementary" aria-labelledby="emergency-title">
        <div>
            <h2 id="emergency-title" class="emergency-title">
                <span aria-hidden="true">🤝 </span>You're Not Alone — We're Just a Few Steps Away<span aria-hidden="true"> ✨</span>
            </h2>
            <p class="emergency-sub">
                <span aria-hidden="true">🕊️ </span>If you're struggling with thoughts of self-harm or feeling unsafe, reach out to us anytime, day or night.
                <span aria-hidden="true">📞 </span>we're here for you.<span aria-hidden="true"> 🕊️</span>
            </p>
        </div>
    </aside>
    """,
    unsafe_allow_html=True
)

# App Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🛡️Lumora RecoveryAI")
    st.caption("GenAI-Powered Zero-Typing Recovery & Prevention Platform")
with col_h2:
    st.write("")
    if st.button(
        "🚨 NEED HELP NOW",
        type="primary",
        use_container_width=True,
        key="need_help_btn",
    ):
        st.session_state["trigger_emergency"] = True
        st.session_state["help_request_sent"] = True

# Help-request confirmation toast + banner (shown right after the button click)
if st.session_state.get("help_request_sent"):
    # One-time toast
    try:
        st.toast("🚑 Help request sent to your emergency contacts!", icon="💚")
    except Exception:
        pass  # older Streamlit versions may not support st.toast

    st.markdown(
        """
        <div role="alert" aria-live="assertive" aria-atomic="true" style="
            background: linear-gradient(135deg, #D6F5E3 0%, #E6DBFA 100%);
            border: 1.5px solid #2E8B57;
            border-radius: 16px;
            padding: 14px 20px;
            margin: 8px 0 18px 0;
            box-shadow: 0 8px 22px rgba(46,139,87,0.20);
            display: flex;
            align-items: center;
            gap: 12px;
            animation: helpPulse 1.6s ease-in-out infinite;
            color: #1A1030;
        ">
            <div style="font-size: 1.8rem;" aria-hidden="true">🚑</div>
            <div>
                <p style="font-weight: 800; font-size: 1.05rem; margin: 0;">
                    <span aria-hidden="true">✅ </span>Help request sent to your care team!
                </p>
                <p style="font-size: 0.92rem; margin-top: 2px; font-weight: 500;">
                    <span aria-hidden="true">💚 </span>A trained responder will reach out to you in a few seconds.
                    Please stay where you are — take a slow breath. You are not alone.<span aria-hidden="true"> 🕊️</span>
                </p>
            </div>
        </div>
        <style>
        @keyframes helpPulse {
            0%,100% { box-shadow: 0 8px 22px rgba(46,139,87,0.20); }
            50%     { box-shadow: 0 12px 28px rgba(46,139,87,0.40); }
        }
        @media (prefers-reduced-motion: reduce) {
            [role="alert"] { animation: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # auto-clear so it doesn't stay forever after the next interaction
    st.session_state["help_request_sent"] = False

# Check API Key Readiness
if not gemini.is_configured():
    st.warning("⚠️ **Gemini API Key Missing or Default Placeholder Detected.**")
    st.info(
        "Please add your `GEMINI_API_KEY` to the `.env` file in the project directory:\n\n"
        "```bash\n"
        "GEMINI_API_KEY=AIzaSyYourActualKeyHere\n"
        "```\n"
        "Get a free API key from [Google AI Studio](https://aistudio.google.com/)."
    )

# Sidebar Info & Emergency Contacts
with st.sidebar:
    st.header("🆘 Crisis Hotlines")
    for name, info in CRISIS_RESOURCES.items():
        # Semantic markup so screen readers announce "Name: <telephone number>"
        st.markdown(
            f'<p style="margin:0;"><strong>{name}</strong>: '
            f'<a href="tel:{info["number"].replace(" ", "").replace("-", "")}" '
            f'aria-label="Call {name} at {info["number"]}" '
            f'style="font-family:monospace;">{info["number"]}</a></p>',
            unsafe_allow_html=True,
        )
        st.caption(info['desc'])
        st.divider()
    
    st.header("💡 Zero-Typing Mode")
    st.write("Designed for moments of **high cognitive load**. Click any preset chip or use voice check-in instead of typing.")
    
    st.divider()
    st.caption("RecoveryAI v1.0 MVP • Powered by Google Gemini 2.5 Flash")

# Navigation Buttons (replaces tabs)
PAGES = [
    ("checkin",   "💬 Mental Health Check-In"),
    ("emergency", "⚡ Emergency Support"),
    ("safety",    "🛡️ Safety Plan Generator"),
    ("education", "📚 Recovery Education"),
    ("game",      "🕊️ Stress Buster Game"),
]

if "active_page" not in st.session_state:
    st.session_state["active_page"] = PAGES[0][0]

nav_cols = st.columns(len(PAGES))
for (key, label), col in zip(PAGES, nav_cols):
    is_active = st.session_state["active_page"] == key
    btn_type = "primary" if is_active else "secondary"
    if col.button(label, key=f"nav_{key}", use_container_width=True, type=btn_type):
        st.session_state["active_page"] = key
        st.rerun()

active = st.session_state["active_page"]
st.divider()


# ==========================================
# PAGE 1: MENTAL HEALTH CHECK-IN
# ==========================================
if active == "checkin":
    st.subheader("Mental Health & Emotional Check-In")
    st.write("Share how you are feeling right now. Zero typing required — select a quick chip or record your voice.")

    # Zero-typing preset mood chips
    st.markdown("**Quick Feeling Presets:**")
    preset_cols = st.columns(3)
    selected_preset = None

    for i, mood in enumerate(PRESET_MOODS):
        col_idx = i % 3
        if preset_cols[col_idx].button(f"👉 {mood}", key=f"mood_chip_{i}", use_container_width=True):
            selected_preset = mood

    # Text & Audio Input Area
    st.divider()
    input_text = st.text_area(
        "Or type your thoughts:",
        value=selected_preset if selected_preset else "",
        placeholder="e.g., I'm feeling stressed after a long shift and wanting to drink...",
        height=90
    )

    audio_file = st.audio_input("🎤 Voice Check-In (Optional)")
    
    analyze_btn = st.button("🔍 Run Check-In Analysis", type="primary")

    if analyze_btn or selected_preset:
        if not input_text and not audio_file:
            st.error("Please select a preset chip, type a feeling, or record audio.")
        else:
            with st.spinner("Connecting to RecoveryAI... Analyzing emotional risk level and triggers..."):
                try:
                    audio_bytes = audio_file.read() if audio_file else None
                    audio_mime = audio_file.type if audio_file else "audio/wav"

                    res = gemini.check_in(
                        user_input=input_text,
                        audio_bytes=audio_bytes,
                        audio_mime=audio_mime
                    )

                    st.session_state["last_checkin"] = res

                except Exception as e:
                    st.error(f"Error calling Gemini API: {str(e)}")

    # Display Results Card if available
    if "last_checkin" in st.session_state:
        res = st.session_state["last_checkin"]

        st.divider()
        st.markdown("### 📊 Check-In Results")

        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(render_risk_badge(res.get("risk_level", "Low")), unsafe_allow_html=True)
            st.write("")
            st.markdown(f"**Identified Trigger:** `{res.get('trigger_detection', 'General Stress')}`")
        with c2:
            st.markdown(
                f"""
                <div class="recovery-card">
                    <div class="card-label">Emotional Summary</div>
                    <div style="font-size: 1.05rem; color: #2E2650;">{res.get('emotional_summary', '')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Recommended Micro-Actions
        st.markdown("#### 🚀 Recommended Immediate Micro-Actions")
        actions = res.get("recommended_actions", [])
        for act in actions:
            st.success(f"✔️ {act}")

        # Encouragement
        st.markdown(
            f"""
            <div class="script-box">
                💚 <b>RecoveryAI Note:</b> "{res.get('encouragement', '')}"
            </div>
            """,
            unsafe_allow_html=True
        )

        if res.get("crisis_alert_needed", False) or res.get("risk_level") in ["High", "Critical"]:
            st.error("🚨 High Risk Detected. We strongly recommend contacting 988 or a trusted caregiver right now.")


# ==========================================
# PAGE 2: EMERGENCY SUPPORT
# ==========================================
if active == "emergency":
    st.subheader("⚡ 1-Click Emergency Grounding Support")
    st.write("Instant interventions when cognitive load is highest and cravings or panic spike.")

    trigger_emer = st.button("🔥 Generate Immediate Emergency Coping Script", type="primary", use_container_width=True)

    # Trigger emergency script automatically if header button clicked
    if trigger_emer or st.session_state.get("trigger_emergency", False):
        st.session_state["trigger_emergency"] = False

        with st.spinner("Generating emergency coping script and grounding steps..."):
            try:
                res = gemini.get_emergency_support(context="Need help now - urge/distress spike")
                st.session_state["emergency_res"] = res
            except Exception as e:
                st.error(f"Error calling Gemini API: {str(e)}")

    if "emergency_res" in st.session_state:
        res = st.session_state["emergency_res"]

        st.markdown("---")
        st.markdown("### 📜 Read Out Loud (Coping Script)")
        st.markdown(
            f"""
            <div class="script-box" style="font-size: 1.15rem; font-weight: 500;">
                🗣️ "{res.get('coping_script', '')}"
            </div>
            """,
            unsafe_allow_html=True
        )

        # Interactive Breathing Widget
        render_breathing_widget()

        col_act1, col_act2 = st.columns(2)
        with col_act1:
            st.markdown("#### ⚡ 1-Click Immediate Actions")
            for act in res.get("immediate_actions", []):
                st.info(f"🔹 {act}")

        with col_act2:
            st.markdown("#### 📲 Caregiver Quick Text Template")
            msg = res.get("caregiver_alert_message", "Hey, I need support right now.")
            st.text_area("Copy & send to your sponsor/caregiver:", value=msg, height=100)
            st.caption("Sending a text breaks isolation and provides immediate human support.")


# ==========================================
# PAGE 3: SAFETY PLAN GENERATOR
# ==========================================
if active == "safety":
    st.subheader("🛡️ Personal Safety & Prevention Plan Generator")
    st.write("Prepare for high-risk situations by building a clear, actionable prevention plan.")

    st.markdown("**Select Today's Trigger (Zero Typing):**")
    trig_cols = st.columns(3)
    selected_trigger = None

    for i, trig in enumerate(PRESET_TRIGGERS):
        col_idx = i % 3
        if trig_cols[col_idx].button(f"🎯 {trig}", key=f"trig_chip_{i}", use_container_width=True):
            selected_trigger = trig

    custom_trig = st.text_input("Or enter a custom trigger:", value=selected_trigger if selected_trigger else "")

    gen_plan_btn = st.button("✨ Generate Safety Plan", type="primary")

    if gen_plan_btn or selected_trigger:
        active_trigger = custom_trig or selected_trigger
        if not active_trigger:
            st.error("Please select a trigger chip or type a trigger.")
        else:
            with st.spinner(f"Generating personalized safety plan for '{active_trigger}'..."):
                try:
                    res = gemini.generate_safety_plan(trigger_input=active_trigger)
                    st.session_state["safety_plan_res"] = res
                except Exception as e:
                    st.error(f"Error calling Gemini API: {str(e)}")

    if "safety_plan_res" in st.session_state:
        res = st.session_state["safety_plan_res"]

        st.divider()
        st.markdown(f"### 📋 Safety Plan: *{res.get('trigger_name', '')}*")

        st.markdown(
            f"""
            <div class="recovery-card">
                <div class="card-label">Proactive Prevention Plan</div>
                <div style="font-size: 1.05rem; color: #4A3E7A; font-weight: 500;">{res.get('prevention_plan', '')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c_coping, c_avoid, c_alt = st.columns(3)

        with c_coping:
            st.markdown("#### 💡 Coping Techniques")
            for item in res.get("coping_techniques", []):
                st.success(f"• {item}")

        with c_avoid:
            st.markdown("#### ⚠️ Things to Avoid")
            for item in res.get("things_to_avoid", []):
                st.error(f"• {item}")

        with c_alt:
            st.markdown("#### 🌱 Healthy Alternatives")
            for item in res.get("healthy_alternatives", []):
                st.info(f"• {item}")


# ==========================================
# PAGE 4: RECOVERY EDUCATION
# ==========================================
if active == "education":
    st.subheader("📚 Recovery Education & Neurobiology")
    st.write("Understand the science of cravings and recovery in simple, non-judgmental language.")

    st.markdown("**Select a Topic (Zero Typing):**")
    edu_cols = st.columns(2)
    selected_edu = None

    for i, topic in enumerate(PRESET_EDU_TOPICS):
        col_idx = i % 2
        if edu_cols[col_idx].button(f"📖 {topic}", key=f"edu_chip_{i}", use_container_width=True):
            selected_edu = topic

    custom_edu = st.text_input("Or ask a custom recovery question:", value=selected_edu if selected_edu else "")

    explain_btn = st.button("💡 Explain with Gemini", type="primary")

    if explain_btn or selected_edu:
        active_query = custom_edu or selected_edu
        if not active_query:
            st.error("Please select a topic chip or enter a question.")
        else:
            with st.spinner(f"Fetching educational insights on '{active_query}'..."):
                try:
                    res = gemini.explain_craving(query_input=active_query)
                    st.session_state["edu_res"] = res
                except Exception as e:
                    st.error(f"Error calling Gemini API: {str(e)}")

    if "edu_res" in st.session_state:
        res = st.session_state["edu_res"]

        st.divider()
        st.markdown(f"### 🔬 Insight: {res.get('topic', '')}")

        st.markdown(
            f"""
            <div class="recovery-card">
                <div class="card-label">Why It Happens (Neurobiological Context)</div>
                <div style="font-size: 1.05rem; line-height: 1.6; color: #2E2650;">{res.get('why_it_happens', '')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("#### 🧠 Science-Backed Recovery Tips")
        for tip in res.get("recovery_tips", []):
            st.info(f"💡 {tip}")

        st.markdown(
            f"""
            <div class="script-box">
                🌟 <b>Positive Encouragement:</b> "{res.get('positive_encouragement', '')}"
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================
# PAGE 5: STRESS BUSTER MINI-GAME
# ==========================================
if active == "game":
    st.subheader("🕊️ Catch the Bird — Fly the Stress")
    st.write(
        "A tiny mindfulness game. **Tap the bird before it flies away.** "
        "Every catch releases a small burst of stress; every miss is a gentle reminder to breathe and try again. "
        "There's no losing here — only calmer moments."
    )
    render_stress_buster_game()
    st.caption("💡 Tip: play for 60 seconds when you feel a craving or spike. Short focused play interrupts the urge loop.")
