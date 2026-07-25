"""
UI Utilities, Styling, Custom CSS, and Grounding Widgets for RecoveryAI Streamlit App.
"""

import streamlit as st

CRISIS_RESOURCES = {
    "988 Lifeline": {"number": "988", "desc": "Suicide & Crisis Lifeline (24/7, Call or Text, Free & Confidential)", "action": "tel:988"},
    "SAMHSA Helpline": {"number": "1-800-662-4357", "desc": "Substance Abuse and Mental Health Services Administration", "action": "tel:18006624357"},
    "Crisis Text Line": {"number": "Text HOME to 741741", "desc": "Free 24/7 Crisis Support via SMS", "action": "sms:741741"}
}

# Zero-typing preset quick options
PRESET_MOODS = [
    "I'm feeling stressed and want to drink.",
    "I feel extremely anxious and overwhelmed right now.",
    "Feeling lonely and missing old habits.",
    "Had an argument with a loved one, feeling triggered.",
    "Exhausted after work, brain is telling me to relax with substances.",
    "Having a sudden strong craving, need grounding."
]

PRESET_TRIGGERS = [
    "Loneliness & Social Isolation",
    "High Work Stress & Burnout",
    "Peer Pressure / Social Settings",
    "Physical Exhaustion / Poor Sleep",
    "Emotional Conflict / Anger",
    "Boredom / Unstructured Free Time",
    "Anniversary of Past Trauma"
]

PRESET_EDU_TOPICS = [
    "Explain My Cravings",
    "Why do cravings feel so intense in the moment?",
    "What happens to dopamine during early recovery?",
    "How does stress trigger the brain's addiction pathway?",
    "What is 'Urge Surfing' and how does it work?",
    "How to handle social pressure without isolating myself"
]


def inject_custom_css():
    """Inject modern, clean, glassmorphism CSS into Streamlit."""
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Top Emergency Banner */
    .emergency-banner {
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        color: white;
        padding: 14px 24px;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(220, 38, 38, 0.35);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .emergency-title {
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin: 0;
    }
    
    .emergency-sub {
        font-size: 0.88rem;
        opacity: 0.92;
        margin-top: 2px;
    }

    /* UI Cards */
    .recovery-card {
        background: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .recovery-card:hover {
        border-color: rgba(16, 185, 129, 0.3);
    }

    /* Card Section Titles */
    .card-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
        color: #94A3B8;
        margin-bottom: 6px;
    }

    /* Risk Badges */
    .risk-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .risk-low {
        background-color: rgba(16, 185, 129, 0.18);
        color: #34D399;
        border: 1px solid #10B981;
    }
    .risk-medium {
        background-color: rgba(245, 158, 11, 0.18);
        color: #FBBF24;
        border: 1px solid #F59E0B;
    }
    .risk-high {
        background-color: rgba(249, 115, 22, 0.18);
        color: #FB923C;
        border: 1px solid #F97316;
    }
    .risk-critical {
        background-color: rgba(239, 68, 68, 0.25);
        color: #F87171;
        border: 1px solid #EF4444;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    /* Coping Script Box */
    .script-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(6, 182, 212, 0.08) 100%);
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 16px 20px;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #E2E8F0;
        font-style: italic;
        margin: 12px 0;
    }

    /* Breathing Widget Container */
    .breathing-box {
        text-align: center;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
    }
    .circle-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    .breath-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.6) 0%, rgba(16, 185, 129, 0.2) 70%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.4);
        animation: breathe 19s infinite ease-in-out;
    }

    @keyframes breathe {
        0% { transform: scale(0.8); opacity: 0.6; }
        21% { transform: scale(1.35); opacity: 1; } /* 4s Inhale */
        58% { transform: scale(1.35); opacity: 0.9; } /* 7s Hold */
        100% { transform: scale(0.8); opacity: 0.6; } /* 8s Exhale */
    }

    /* Custom Streamlit Button Tweaks */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def render_risk_badge(risk_level: str) -> str:
    """Return HTML string for risk level badge."""
    level = (risk_level or "Low").lower()
    badge_class = f"risk-{level}"
    return f'<span class="risk-badge {badge_class}">Risk Level: {risk_level}</span>'


def render_breathing_widget():
    """Render animated 4-7-8 breathing circle."""
    html = """
    <div class="breathing-box">
        <h4 style="margin: 0; color: #38BDF8;">🫁 4-7-8 Grounding Breathing Exercise</h4>
        <p style="font-size: 0.88rem; color: #94A3B8; margin-top: 4px;">Inhale quietly through nose (4s) • Hold breath (7s) • Exhale completely through mouth (8s)</p>
        <div class="circle-container">
            <div class="breath-circle">Breathe</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
