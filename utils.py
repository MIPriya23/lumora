"""
UI Utilities, Styling, Custom CSS, and Grounding Widgets for RecoveryAI Streamlit App.
"""

import streamlit as st
import streamlit.components.v1 as components

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
    """Inject pastel-palette, high-contrast, accessible, gently animated CSS."""
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* =========================================================
       ACCESSIBILITY: honour user's reduced-motion preference.
       Disables every decorative animation/transition for people
       with vestibular disorders or motion sensitivity (WCAG 2.3.3).
       ========================================================= */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.001ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.001ms !important;
            scroll-behavior: auto !important;
        }
    }

    /* Visible keyboard focus ring on every interactive element (WCAG 2.4.7) */
    a:focus-visible,
    button:focus-visible,
    input:focus-visible,
    textarea:focus-visible,
    select:focus-visible,
    [role="button"]:focus-visible,
    [tabindex]:focus-visible {
        outline: 3px solid #6C4DBA !important;
        outline-offset: 2px !important;
        box-shadow: 0 0 0 4px rgba(108,77,186,0.30) !important;
        border-radius: 10px;
    }

    /* Screen-reader-only helper */
    .sr-only {
        position: absolute !important;
        width: 1px !important; height: 1px !important;
        padding: 0 !important; margin: -1px !important;
        overflow: hidden !important; clip: rect(0,0,0,0) !important;
        white-space: nowrap !important; border: 0 !important;
    }

    /* =========================================================
       PASTEL PALETTE + CONTRAST INK PAIRS
       Surfaces (light pastel):
         rose    #FFD6E1   lavender #E6DBFA   sky     #D6ECFB
         mint    #D6F5E3   peach    #FFE5D0   cream   #FFF6E0
       Ink (deep contrast text):
         primary #2E2650   secondary #4A3E7A   accent  #6C4DBA
         success #0F5132   warning   #6B4A00   danger  #7A0F2A
       ========================================================= */

    html, body, [class*="css"], .stApp, .stMarkdown, p, span, li, label {
        font-family: 'Quicksand', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #2E2650 !important;
    }

    /* Animated pastel gradient background */
    .stApp {
        background: linear-gradient(-45deg, #FFE0EC, #E6DBFA, #D6ECFB, #D6F5E3, #FFE5D0);
        background-size: 400% 400%;
        animation: pastelShift 24s ease infinite;
        /* create a stacking context so decorative ::before stays behind
           content WITHOUT us having to touch position on sidebar/main */
        isolation: isolate;
    }
    @keyframes pastelShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Mild sparkles (twinkling dots) — decorative layer BEHIND content */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: -1;
        background-image:
            radial-gradient(1.6px 1.6px at 10% 20%, #ffffff 100%, transparent),
            radial-gradient(1.4px 1.4px at 25% 65%, #ffffff 100%, transparent),
            radial-gradient(1.8px 1.8px at 40% 30%, #ffffff 100%, transparent),
            radial-gradient(1.2px 1.2px at 55% 80%, #ffffff 100%, transparent),
            radial-gradient(1.6px 1.6px at 70% 15%, #ffffff 100%, transparent),
            radial-gradient(1.4px 1.4px at 85% 55%, #ffffff 100%, transparent),
            radial-gradient(1.2px 1.2px at 92% 88%, #ffffff 100%, transparent),
            radial-gradient(1.4px 1.4px at 15% 90%, #ffffff 100%, transparent),
            radial-gradient(1.8px 1.8px at 60% 45%, #ffffff 100%, transparent),
            radial-gradient(1.2px 1.2px at 33% 10%, #ffffff 100%, transparent);
        opacity: 0.55;
        animation: twinkle 3.6s ease-in-out infinite;
    }
    @keyframes twinkle {
        0%, 100% { opacity: 0.15; }
        50%      { opacity: 0.7;  }
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Headings — deep purple ink for strong contrast on pastel */
    h1, h2, h3, h4, h5, h6 {
        color: #2E2650 !important;
        font-family: 'Quicksand', sans-serif !important;
        letter-spacing: 0.2px;
        font-weight: 700 !important;
    }
    h1 { text-shadow: 0 2px 12px rgba(108,77,186,0.15); }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF0F6 0%, #EDE3FB 100%) !important;
        border-right: 1px solid rgba(108,77,186,0.18);
    }
    [data-testid="stSidebar"] * { color: #2E2650 !important; }

    /* Top Streamlit header bar — pastel surface */
    [data-testid="stHeader"],
    header[data-testid="stHeader"] {
        background: linear-gradient(90deg, #FFE0EC 0%, #E6DBFA 50%, #D6ECFB 100%) !important;
        border-bottom: 1px solid rgba(108,77,186,0.25);
        box-shadow: 0 2px 10px rgba(108,77,186,0.10);
        position: relative;
    }

    /* HIDE default header icons/buttons (menu, deploy, decoration strip) — keep status widget */
    [data-testid="stMainMenu"],
    [data-testid="stDeployButton"],
    [data-testid="stDecoration"],
    header [data-testid="baseButton-header"],
    header [data-testid="baseButton-headerNoPadding"]:not([kind="headerNoPadding"]) {
        display: none !important;
    }

    /* --- IDLE STATE: Always-visible "Stable Man" attached to the header --- */
    [data-testid="stHeader"]::after {
        content: "🧍 RecoveryAI";
        position: absolute;
        top: 50%;
        right: 18px;
        transform: translateY(-50%);
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        background: linear-gradient(135deg, #FFF0F6, #E6DBFA);
        border: 1.5px solid #6C4DBA;
        border-radius: 999px;
        color: #1A1030;
        font-family: 'Quicksand', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 14px rgba(108,77,186,0.25);
        animation: standIdle 3.2s ease-in-out infinite;
        pointer-events: none;
        z-index: 2;
    }
    @keyframes standIdle {
        0%,100% { transform: translateY(-50%)             scale(1);    }
        50%     { transform: translateY(calc(-50% - 2px)) scale(1.02); }
    }

    /* When Streamlit is running, its stStatusWidget appears inside the header.
       Hide the idle stable-man so only the running-man is visible. */
    [data-testid="stHeader"]:has([data-testid="stStatusWidget"])::after {
        display: none !important;
    }

    /* --- RUNNING STATE: Custom "Running Man" indicator ---
       Streamlit auto-shows stStatusWidget only while the script is executing,
       and auto-hides it when idle — so the stable man returns automatically. */
    [data-testid="stStatusWidget"] {
        background: linear-gradient(135deg, #FFF0F6, #E6DBFA) !important;
        border: 1.5px solid #6C4DBA !important;
        border-radius: 999px !important;
        padding: 4px 14px 4px 10px !important;
        color: #1A1030 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(108,77,186,0.25) !important;
        display: flex !important;
        align-items: center;
        gap: 8px;
        overflow: hidden;
    }
    /* Hide Streamlit's default icon + text inside the widget */
    [data-testid="stStatusWidget"] > * {
        display: none !important;
    }
    /* Inject animated running-man + label */
    [data-testid="stStatusWidget"]::before {
        content: "🏃";
        font-size: 1.5rem;
        line-height: 1;
        display: inline-block;
        animation: runMan 0.55s ease-in-out infinite;
    }
    [data-testid="stStatusWidget"]::after {
        content: "Running…";
        color: #1A1030 !important;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.3px;
        animation: pulseText 1.4s ease-in-out infinite;
    }
    @keyframes runMan {
        0%   { transform: translateX(0)   translateY(0)   rotate(-4deg); }
        25%  { transform: translateX(3px) translateY(-2px) rotate(2deg);  }
        50%  { transform: translateX(6px) translateY(0)   rotate(-4deg); }
        75%  { transform: translateX(3px) translateY(-2px) rotate(2deg);  }
        100% { transform: translateX(0)   translateY(0)   rotate(-4deg); }
    }
    @keyframes pulseText {
        0%,100% { opacity: 0.75; }
        50%     { opacity: 1;    }
    }

    /* Emergency banner — dreamy multi-pastel surface with deep purple ink */
    .emergency-banner {
        background: linear-gradient(135deg,
            #E6DBFA 0%,    /* lavender */
            #D6ECFB 35%,   /* sky */
            #D6F5E3 65%,   /* mint */
            #FFE5D0 100%   /* peach */
        );
        background-size: 200% 200%;
        animation: bannerGlow 6s ease-in-out infinite, bannerShift 14s ease-in-out infinite;
        color: #2E2650;
        padding: 16px 26px;
        border-radius: 20px;
        box-shadow:
            0 10px 28px rgba(108,77,186,0.20),
            0 0 0 1px rgba(255,255,255,0.85) inset;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        border: 1px solid rgba(108,77,186,0.28);
    }
    @keyframes bannerGlow {
        0%,100% { box-shadow: 0 10px 28px rgba(108,77,186,0.20), 0 0 0 1px rgba(255,255,255,0.85) inset; }
        50%     { box-shadow: 0 16px 36px rgba(139,111,216,0.35), 0 0 0 1px rgba(255,255,255,0.95) inset; }
    }
    @keyframes bannerShift {
        0%,100% { background-position: 0% 50%; }
        50%     { background-position: 100% 50%; }
    }
    .emergency-title {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 0.4px;
        margin: 0;
        color: #1A1030 !important;
        text-shadow: 0 1px 0 rgba(255,255,255,0.6);
    }
    .emergency-sub {
        font-size: 0.92rem;
        opacity: 1;
        margin-top: 4px;
        color: #2E2650 !important;
        font-weight: 500;
    }

    /* Cards — soft white glass with deep ink text (high contrast) */
    .recovery-card {
        background: rgba(255, 255, 255, 0.72);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(108,77,186,0.20);
        border-radius: 18px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: 0 10px 30px rgba(108,77,186,0.15);
        transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
        animation: floatCard 7s ease-in-out infinite;
    }
    .recovery-card:hover {
        transform: translateY(-4px);
        border-color: #6C4DBA;
        box-shadow: 0 18px 40px rgba(108,77,186,0.25);
    }
    @keyframes floatCard {
        0%,100% { transform: translateY(0); }
        50%     { transform: translateY(-3px); }
    }

    /* Card label — deep purple for readable meta text */
    .card-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 800;
        color: #4A3E7A;
        margin-bottom: 6px;
    }

    /* Risk Badges — pastel surface + deep matching ink */
    .risk-badge {
        display: inline-block;
        padding: 8px 18px;
        border-radius: 22px;
        font-weight: 800;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    }
    .risk-low {
        background: linear-gradient(135deg, #D6F5E3, #A8E8C4);
        color: #0F5132;
        border: 2px solid #2E8B57;
    }
    .risk-medium {
        background: linear-gradient(135deg, #FFF3C7, #FFE28A);
        color: #6B4A00;
        border: 2px solid #B8860B;
    }
    .risk-high {
        background: linear-gradient(135deg, #FFDFC4, #FFBE8A);
        color: #7A3A00;
        border: 2px solid #C25A00;
    }
    .risk-critical {
        background: linear-gradient(135deg, #FFC5D3, #FF9FB6);
        color: #6B0A22;
        border: 2px solid #C71E4F;
        animation: pulseSoft 2.2s infinite;
    }
    @keyframes pulseSoft {
        0%   { box-shadow: 0 0 0 0 rgba(199,30,79,0.5); }
        70%  { box-shadow: 0 0 0 14px rgba(199,30,79,0); }
        100% { box-shadow: 0 0 0 0 rgba(199,30,79,0); }
    }

    /* Script box — lavender/sky pastel, deep ink text */
    .script-box {
        background: linear-gradient(135deg, rgba(230,219,250,0.85), rgba(214,236,251,0.85));
        border-left: 5px solid #6C4DBA;
        border-radius: 14px;
        padding: 18px 22px;
        font-size: 1.05rem;
        line-height: 1.65;
        color: #2E2650;
        font-style: italic;
        margin: 12px 0;
        box-shadow: 0 6px 20px rgba(108,77,186,0.18);
    }

    /* Breathing widget */
    .breathing-box {
        text-align: center;
        background: linear-gradient(160deg, rgba(255,255,255,0.82), rgba(230,219,250,0.65));
        border: 1px solid rgba(108,77,186,0.30);
        border-radius: 20px;
        padding: 26px;
        margin: 16px 0;
        box-shadow: 0 10px 28px rgba(108,77,186,0.15);
    }
    .circle-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    .breath-circle {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle, #FFD6E1 0%, #E6DBFA 55%, #D6ECFB 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #2E2650;
        font-weight: 800;
        font-size: 1rem;
        border: 2px solid rgba(255,255,255,0.9);
        box-shadow: 0 0 30px rgba(108,77,186,0.45), 0 0 60px rgba(255,214,225,0.35);
        animation: breathe 19s infinite ease-in-out, hueShift 12s linear infinite;
    }
    @keyframes breathe {
        0%   { transform: scale(0.85); opacity: 0.75; }
        21%  { transform: scale(1.35); opacity: 1;    } /* 4s inhale */
        58%  { transform: scale(1.35); opacity: 0.95; } /* 7s hold */
        100% { transform: scale(0.85); opacity: 0.75; } /* 8s exhale */
    }
    @keyframes hueShift {
        0%,100% { filter: hue-rotate(0deg); }
        50%     { filter: hue-rotate(25deg); }
    }

    /* Buttons — pastel gradient, dark ink text for contrast */
    .stButton>button {
        border-radius: 14px !important;
        font-weight: 700 !important;
        color: #2E2650 !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #F0E7FB 100%) !important;
        border: 1.5px solid #B9A7EA !important;
        box-shadow: 0 6px 16px rgba(108,77,186,0.18) !important;
        transition: all 0.25s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #FFF0F6 0%, #E6DBFA 100%) !important;
        border-color: #6C4DBA !important;
        box-shadow: 0 10px 22px rgba(108,77,186,0.30) !important;
    }
    .stButton>button:active { transform: translateY(0); }

    /* Primary button — deeper pastel with white text for max contrast */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #8B6FD8 0%, #E85A82 100%) !important;
        color: #FFFFFF !important;
        border: 1.5px solid rgba(255,255,255,0.7) !important;
        box-shadow: 0 8px 22px rgba(139,111,216,0.45) !important;
    }
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7A5EC7 0%, #D64872 100%) !important;
        box-shadow: 0 12px 28px rgba(139,111,216,0.55) !important;
    }

    /* Text inputs / textareas — clean pastel */
    .stTextInput input, .stTextArea textarea {
        background: rgba(255,255,255,0.85) !important;
        color: #2E2650 !important;
        border: 1.5px solid rgba(108,77,186,0.30) !important;
        border-radius: 12px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6C4DBA !important;
        box-shadow: 0 0 0 3px rgba(108,77,186,0.25) !important;
    }

    /* Tabs — pastel pills */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.55);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.85);
        backdrop-filter: blur(8px);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        color: #4A3E7A !important;
        font-weight: 700 !important;
        padding: 8px 16px !important;
        transition: all 0.25s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(230,219,250,0.7) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD6E1, #E6DBFA) !important;
        color: #2E2650 !important;
        box-shadow: 0 4px 12px rgba(108,77,186,0.30);
    }

    /* Streamlit alert boxes — pastel with deep ink */
    div[data-testid="stAlert"] {
        border-radius: 14px !important;
        border: 1.5px solid rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(10px);
        color: #2E2650 !important;
    }
    div[data-testid="stAlert"] * { color: #2E2650 !important; }

    /* Divider */
    hr { border-color: rgba(108,77,186,0.25) !important; }

    /* Caption */
    .stCaption, [data-testid="stCaptionContainer"] { color: #4A3E7A !important; }

    /* Toasts (st.toast) — pastel with dark ink */
    [data-testid="stToast"],
    [data-testid="stToastContainer"] [data-testid="stToast"],
    div[data-baseweb="toast"],
    div[role="alert"][data-baseweb="toast"] {
        background: linear-gradient(135deg, #FFF6FA 0%, #E6DBFA 100%) !important;
        background-color: #FFF6FA !important;
        color: #1A1030 !important;
        border: 1.5px solid #6C4DBA !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 26px rgba(108,77,186,0.30) !important;
        backdrop-filter: blur(8px);
    }
    [data-testid="stToast"] *,
    div[data-baseweb="toast"] * {
        color: #1A1030 !important;
        background-color: transparent !important;
    }
    [data-testid="stToast"] svg,
    div[data-baseweb="toast"] svg {
        color: #6C4DBA !important;
        fill: #6C4DBA !important;
        stroke: #6C4DBA !important;
        opacity: 1 !important;
    }

    /* Inline code (backticks in markdown, e.g. phone numbers) — pastel pill */
    code, .stMarkdown code, [data-testid="stMarkdownContainer"] code {
        background: linear-gradient(135deg, #FFF0F6, #E6DBFA) !important;
        color: #1A1030 !important;
        border: 1px solid #B9A7EA !important;
        border-radius: 8px !important;
        padding: 2px 8px !important;
        font-family: 'Quicksand', 'Inter', monospace !important;
        font-weight: 700 !important;
        font-size: 0.92em !important;
        box-shadow: 0 2px 6px rgba(108,77,186,0.15) !important;
    }
    /* Code blocks (```...```) — soft pastel surface */
    pre, .stMarkdown pre, [data-testid="stMarkdownContainer"] pre {
        background: rgba(255,255,255,0.75) !important;
        border: 1px solid rgba(108,77,186,0.25) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    pre code, pre > code {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #1A1030 !important;
        padding: 0 !important;
    }
    /* Sidebar inline code — same pastel style */
    [data-testid="stSidebar"] code {
        background: linear-gradient(135deg, #FFF0F6, #E6DBFA) !important;
        color: #1A1030 !important;
        border: 1px solid #B9A7EA !important;
    }

    /* Audio input (voice recorder) — pastel themed, force light backgrounds
       on every nested container (Streamlit ships a dark inner shell by default). */
    [data-testid="stAudioInput"],
    .stAudioInput,
    [data-testid="stAudioInput"] > div,
    [data-testid="stAudioInput"] > div > div,
    [data-testid="stAudioInput"] section,
    [data-testid="stAudioInput"] [class*="AudioInput"],
    [data-testid="stAudioInput"] [class*="stAudio"] {
        background: linear-gradient(135deg, #FFF6FA 0%, #EDE3FB 100%) !important;
        border: 1.5px solid #B9A7EA !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 14px rgba(108,77,186,0.15) !important;
    }
    /* Inner rows/toolbars — transparent so they inherit the pastel surface */
    [data-testid="stAudioInput"] div,
    [data-testid="stAudioInput"] section > div {
        background-color: transparent !important;
    }

    /* Record / play / delete buttons — pastel pill with dark icon */
    [data-testid="stAudioInput"] button,
    [data-testid="stAudioInput"] [role="button"] {
        background: #FFFFFF !important;
        border: 1.5px solid #6C4DBA !important;
        color: #1A1030 !important;
        border-radius: 999px !important;
        box-shadow: 0 3px 10px rgba(108,77,186,0.20) !important;
    }
    [data-testid="stAudioInput"] button:hover,
    [data-testid="stAudioInput"] [role="button"]:hover {
        background: linear-gradient(135deg, #FFD6E1, #E6DBFA) !important;
        border-color: #4A3E7A !important;
    }

    /* All icons + text inside → deep ink */
    [data-testid="stAudioInput"] * {
        color: #1A1030 !important;
    }
    [data-testid="stAudioInput"] svg {
        color: #1A1030 !important;
        fill: #1A1030 !important;
        stroke: #1A1030 !important;
        opacity: 1 !important;
    }
    [data-testid="stAudioInput"] button:hover svg {
        color: #6C4DBA !important;
        fill: #6C4DBA !important;
        stroke: #6C4DBA !important;
    }

    /* Waveform / progress canvas — light pastel track */
    [data-testid="stAudioInput"] canvas {
        background: rgba(255,255,255,0.6) !important;
        border-radius: 8px;
    }
    [data-testid="stAudioInput"] [class*="waveSurfer"],
    [data-testid="stAudioInput"] [class*="progress"] {
        background: rgba(255,255,255,0.5) !important;
    }

    /* Audio playback element (<audio>) once recording is done */
    [data-testid="stAudioInput"] audio {
        background: #FFFFFF !important;
        border-radius: 999px !important;
        filter: none !important;
    }
    /* Timer / duration display — force pastel bg, dark ink text */
    [data-testid="stAudioInput"] time,
    [data-testid="stAudioInput"] span,
    [data-testid="stAudioInput"] p,
    [data-testid="stAudioInput"] label,
    [data-testid="stAudioInput"] [class*="Time"],
    [data-testid="stAudioInput"] [class*="time"],
    [data-testid="stAudioInput"] [class*="Duration"],
    [data-testid="stAudioInput"] [class*="duration"],
    [data-testid="stAudioInput"] [class*="Timer"],
    [data-testid="stAudioInput"] [class*="timer"],
    [data-testid="stAudioInput"] [class*="Counter"],
    [data-testid="stAudioInput"] [class*="counter"] {
        background: rgba(255,255,255,0.9) !important;
        background-color: rgba(255,255,255,0.9) !important;
        background-image: none !important;
        color: #1A1030 !important;
        border-radius: 8px !important;
        padding: 2px 8px !important;
        font-weight: 700 !important;
        font-variant-numeric: tabular-nums;
    }
    /* Nuke any dark inline bg on ANY descendant of the audio input */
    [data-testid="stAudioInput"] * {
        background-color: transparent !important;
    }
    /* Then explicitly restore the pastel look on the elements that need a surface */
    [data-testid="stAudioInput"],
    [data-testid="stAudioInput"] > div,
    [data-testid="stAudioInput"] > div > div,
    [data-testid="stAudioInput"] section {
        background: linear-gradient(135deg, #FFF6FA 0%, #EDE3FB 100%) !important;
    }
    [data-testid="stAudioInput"] button,
    [data-testid="stAudioInput"] [role="button"] {
        background: #FFFFFF !important;
    }
    [data-testid="stAudioInput"] button:hover,
    [data-testid="stAudioInput"] [role="button"]:hover {
        background: linear-gradient(135deg, #FFD6E1, #E6DBFA) !important;
    }
    [data-testid="stAudioInput"] time,
    [data-testid="stAudioInput"] [class*="Time"],
    [data-testid="stAudioInput"] [class*="time"],
    [data-testid="stAudioInput"] [class*="Duration"],
    [data-testid="stAudioInput"] [class*="duration"],
    [data-testid="stAudioInput"] [class*="Timer"],
    [data-testid="stAudioInput"] [class*="timer"] {
        background: rgba(255,255,255,0.9) !important;
    }
    /* Fallback: kill any remaining dark filter */
    [data-testid="stAudioInput"] [style*="background"] {
        background-color: transparent !important;
    }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def render_risk_badge(risk_level: str) -> str:
    """Return accessible HTML for a risk-level badge.

    Uses BOTH color AND a shape/symbol so colorblind users can
    distinguish severity (WCAG 1.4.1 — Use of Color).
    """
    level = (risk_level or "Low").lower()
    badge_class = f"risk-{level}"
    symbols = {
        "low":      "\u25CB",   # ○  hollow circle
        "medium":   "\u25D0",   # ◐  half-filled circle
        "high":     "\u25D1",   # ◑  mostly-filled circle
        "critical": "\u25CF",   # ●  solid filled circle
    }
    symbol = symbols.get(level, "\u25CB")
    return (
        f'<span class="risk-badge {badge_class}" '
        f'role="status" aria-live="polite" '
        f'aria-label="Risk level: {risk_level}">'
        f'<span aria-hidden="true" style="margin-right:6px;">{symbol}</span>'
        f'Risk Level: {risk_level}'
        f'</span>'
    )


def render_breathing_widget():
    """Render animated 4-7-8 breathing circle (accessible)."""
    html = """
    <section class="breathing-box" role="region" aria-label="4-7-8 breathing exercise">
        <h3 style="margin: 0; color: #2E2650; font-size: 1.15rem;">
            <span aria-hidden="true">🫁 </span>4-7-8 Grounding Breathing Exercise
        </h3>
        <p style="font-size: 0.9rem; color: #4A3E7A; margin-top: 4px; font-weight: 500;">
            Inhale quietly through nose (4 seconds) • Hold breath (7 seconds) • Exhale completely through mouth (8 seconds)
        </p>
        <div class="circle-container" aria-hidden="true">
            <div class="breath-circle">Breathe</div>
        </div>
        <span class="sr-only">
            A visual pastel circle expands during inhale, holds during breath-hold, and contracts during exhale.
            This decoration repeats every nineteen seconds and can be paused by enabling reduced motion in your operating system.
        </span>
    </section>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_stress_buster_game():
    """Render the 'Catch the Bird — Fly the Stress' mini-game."""
    game_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      * { box-sizing: border-box; }
      body { margin: 0; font-family: 'Quicksand', system-ui, sans-serif; }
      .game-wrap {
        background: linear-gradient(180deg, #D6ECFB 0%, #E6DBFA 55%, #FFE0EC 100%);
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 10px 30px rgba(108,77,186,0.15);
        border: 1.5px solid rgba(108,77,186,0.25);
      }
      .hud {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
        color: #1A1030;
        font-weight: 700;
      }
      .hud .chip {
        background: rgba(255,255,255,0.85);
        border: 1.5px solid #B9A7EA;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.9rem;
        box-shadow: 0 3px 10px rgba(108,77,186,0.15);
      }
      .hud .chip .num { color: #6C4DBA; margin-left: 6px; }
      #startBtn, #stopBtn {
        color: #fff;
        border: none;
        padding: 8px 18px;
        border-radius: 999px;
        font-weight: 800;
        cursor: pointer;
        transition: transform .15s ease, opacity .2s ease;
      }
      #startBtn {
        background: linear-gradient(135deg, #8B6FD8, #E85A82);
        box-shadow: 0 6px 16px rgba(139,111,216,0.45);
      }
      #stopBtn {
        background: linear-gradient(135deg, #F4A6B8, #C71E4F);
        box-shadow: 0 6px 16px rgba(199,30,79,0.35);
        margin-left: 6px;
      }
      #startBtn:hover, #stopBtn:hover { transform: translateY(-2px); }
      #stopBtn:disabled {
        opacity: 0.45;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
      }
      #arena {
        position: relative;
        width: 100%;
        height: 380px;
        background:
          radial-gradient(circle at 20% 30%, rgba(255,255,255,0.55) 0 3px, transparent 4px),
          radial-gradient(circle at 65% 20%, rgba(255,255,255,0.55) 0 2px, transparent 3px),
          radial-gradient(circle at 45% 60%, rgba(255,255,255,0.45) 0 2px, transparent 3px),
          radial-gradient(circle at 80% 55%, rgba(255,255,255,0.55) 0 3px, transparent 4px),
          linear-gradient(180deg, #E9F4FF 0%, #F6ECFF 60%, #FFEDF3 100%);
        border-radius: 16px;
        overflow: hidden;
        border: 1.5px solid rgba(108,77,186,0.25);
        cursor: crosshair;
      }
      #bird {
        position: absolute;
        font-size: 2.8rem;
        line-height: 1;
        user-select: none;
        cursor: pointer;
        transition: transform .12s ease;
        filter: drop-shadow(0 3px 6px rgba(108,77,186,0.35));
        will-change: transform, left, top;
        /* Bigger invisible hit area around the emoji */
        padding: 14px;
        border-radius: 50%;
        z-index: 5;
      }
      #bird:hover { transform: scale(1.15) rotate(-6deg); }
      #bird:focus-visible {
        outline: 3px solid #6C4DBA;
        outline-offset: 6px;
        box-shadow: 0 0 0 6px rgba(108,77,186,0.35);
        border-radius: 50%;
      }
      .cloud {
        position: absolute;
        font-size: 2rem;
        opacity: .5;
        animation: drift 22s linear infinite;
        pointer-events: none;   /* never intercept bird clicks */
        z-index: 1;
      }
      .cloud.c1 { top: 12%; left: -10%; animation-duration: 28s; }
      .cloud.c2 { top: 35%; left: -30%; animation-duration: 42s; font-size: 2.6rem; opacity:.35; }
      .cloud.c3 { top: 68%; left: -50%; animation-duration: 36s; font-size: 1.6rem; opacity:.55; }
      @keyframes drift {
        from { transform: translateX(0); }
        to   { transform: translateX(150vw); }
      }
      #msg {
        margin-top: 12px;
        min-height: 44px;
        padding: 10px 14px;
        border-radius: 12px;
        background: rgba(255,255,255,0.85);
        border-left: 5px solid #6C4DBA;
        color: #1A1030;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 14px rgba(108,77,186,0.12);
        transition: all .25s ease;
      }
      #msg.win  { border-left-color: #2E8B57; background: linear-gradient(135deg,#EAF7EF,#FFFFFF); }
      #msg.miss { border-left-color: #E85A82; background: linear-gradient(135deg,#FFEEF3,#FFFFFF); }
      .fall { animation: fall 1.2s ease-in forwards; }
      @keyframes fall {
        0%   { transform: translateY(0)    rotate(0deg);   opacity: 1; }
        60%  { transform: translateY(240px) rotate(180deg); opacity: 1; }
        100% { transform: translateY(340px) rotate(360deg); opacity: 0; }
      }
      .caught { animation: caught .5s ease-out forwards; }
      @keyframes caught {
        0%   { transform: scale(1);   filter: hue-rotate(0);   }
        50%  { transform: scale(1.6); filter: hue-rotate(60deg); }
        100% { transform: scale(0);   opacity: 0; }
      }
      .spark {
        position: absolute;
        pointer-events: none;
        font-size: 1.2rem;
        animation: sparkOut .9s ease-out forwards;
      }
      @keyframes sparkOut {
        0%   { transform: translate(-50%,-50%) scale(.4); opacity: 1; }
        100% { transform: translate(var(--dx), var(--dy)) scale(1.4); opacity: 0; }
      }
    </style>
    </head>
    <body>
      <div class="game-wrap" role="region" aria-label="Stress buster bird-catching mini game">
        <div class="hud">
          <div class="chip" aria-live="polite" aria-atomic="true">
            <span aria-hidden="true">🏆 </span>Caught: <span class="num" id="score">0</span>
          </div>
          <div class="chip" aria-live="polite" aria-atomic="true">
            <span aria-hidden="true">🔥 </span>Streak: <span class="num" id="streak">0</span>
          </div>
          <div class="chip" aria-live="polite" aria-atomic="true">
            <span aria-hidden="true">🎯 </span>Best: <span class="num" id="best">0</span>
          </div>
          <button id="startBtn" aria-label="Start the stress-buster game">
            <span aria-hidden="true">▶ </span>Start
          </button>
          <button id="stopBtn" disabled aria-label="Stop the game">
            <span aria-hidden="true">⏹ </span>Stop
          </button>
        </div>
        <div id="arena" role="application" aria-label="Game arena. When a bird appears, press Space or Enter to catch it.">
          <div class="cloud c1" aria-hidden="true">☁️</div>
          <div class="cloud c2" aria-hidden="true">☁️</div>
          <div class="cloud c3" aria-hidden="true">☁️</div>
        </div>
        <div id="msg" role="status" aria-live="polite">
          <span aria-hidden="true">🕊️ </span>Click <b>Start</b>, then tap or press Space/Enter on the bird before it flies away. Every catch releases a little stress!
        </div>
      </div>

    <script>
      const WINS = [
        "🌟 Beautiful catch! One less worry in your mind.",
        "💚 You did it! Notice how good that little win feels.",
        "✨ Stress released! Your focus is stronger than you think.",
        "🌈 Nice reflexes! You're capable of more than the anxiety says.",
        "🕊️ Freedom! You're building resilience one catch at a time.",
        "🎉 Yes! Small wins add up to big recovery.",
        "💜 Wonderful — you showed up for yourself just now."
      ];
      const MISSES = [
        "🌸 It's okay — even the calm sky has clouds. Try again!",
        "💙 Missing is part of learning. Breathe and go again.",
        "🌿 Progress > perfection. Reset and try once more.",
        "🤍 Be gentle with yourself. The next bird is yours.",
        "🌻 One miss means nothing. You showed up — that's what matters.",
        "💫 Everyone slips. What counts is that you're still here."
      ];

      const BIRDS = ["🕊️","🐦","🐤","🦜","🐥"];
      const arena  = document.getElementById('arena');
      const msg    = document.getElementById('msg');
      const scoreEl= document.getElementById('score');
      const streakEl= document.getElementById('streak');
      const bestEl = document.getElementById('best');
      const startBtn= document.getElementById('startBtn');
      const stopBtn = document.getElementById('stopBtn');

      let score = 0, streak = 0, best = 0, playing = false;
      let bird = null, moveTimer = null, lifeTimer = null;

      function setMsg(text, cls) {
        msg.className = ''; if (cls) msg.classList.add(cls);
        msg.innerHTML = text;
      }
      function rand(min, max) { return Math.random() * (max - min) + min; }
      function pick(arr) { return arr[Math.floor(Math.random()*arr.length)]; }

      function placeBird() {
        const w = arena.clientWidth, h = arena.clientHeight;
        const x = rand(20, w - 60);
        const y = rand(20, h - 100);
        bird.style.left = x + 'px';
        bird.style.top  = y + 'px';
      }

      function sparkleAt(x, y) {
        for (let i=0;i<8;i++){
          const s = document.createElement('div');
          s.className = 'spark';
          s.textContent = pick(['✨','💚','⭐','💜','🌸']);
          s.style.left = x + 'px'; s.style.top = y + 'px';
          const ang = (i/8)*Math.PI*2;
          s.style.setProperty('--dx', Math.cos(ang)*70 + 'px');
          s.style.setProperty('--dy', Math.sin(ang)*70 + 'px');
          arena.appendChild(s);
          setTimeout(()=>s.remove(), 900);
        }
      }

      function catchBird(e) {
        if (!bird || bird.dataset.caught === '1') return;
        bird.dataset.caught = '1';
        e.preventDefault();
        e.stopPropagation();
        const rect  = bird.getBoundingClientRect();
        const aRect = arena.getBoundingClientRect();
        sparkleAt(rect.left - aRect.left + rect.width/2, rect.top - aRect.top + rect.height/2);
        bird.classList.add('caught');
        score++; streak++; best = Math.max(best, streak);
        scoreEl.textContent = score;
        streakEl.textContent = streak;
        bestEl.textContent = best;
        setMsg(pick(WINS), 'win');
        clearTimers();
        setTimeout(() => { if (playing) spawnBird(); }, 500);
      }

      function missBird() {
        if (!bird) return;
        streak = 0; streakEl.textContent = 0;
        bird.classList.add('fall');
        setMsg(pick(MISSES), 'miss');
        clearTimers();
        setTimeout(() => { if (playing) spawnBird(); }, 1300);
      }

      function clearTimers() {
        if (moveTimer) { clearTimeout(moveTimer); moveTimer = null; }
        if (lifeTimer) { clearTimeout(lifeTimer); lifeTimer = null; }
      }

      function spawnBird() {
        if (bird) bird.remove();
        bird = document.createElement('div');
        bird.id = 'bird';
        bird.textContent = pick(BIRDS);
        // Accessibility: keyboard-focusable, screen-reader labelled
        bird.setAttribute('role', 'button');
        bird.setAttribute('tabindex', '0');
        bird.setAttribute('aria-label', 'Catch the flying bird. Press Space or Enter.');
        // Register on pointerdown (fast) + click (touch) + keyboard (Enter/Space)
        bird.addEventListener('pointerdown', catchBird);
        bird.addEventListener('click', catchBird);
        bird.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ' || e.code === 'Space') {
                e.preventDefault();
                catchBird(e);
            }
        });
        arena.appendChild(bird);
        placeBird();
        bird.focus();  // let keyboard users act immediately

        // Give the player a short grace period to land the first click, then start flitting
        const interval = Math.max(550, 1100 - streak*45);
        moveTimer = setTimeout(function loop(){
            if (!playing || !bird) return;
            placeBird();
            moveTimer = setTimeout(loop, interval);
        }, 700);

        // If not caught in N seconds, it falls
        const life = Math.max(2500, 5000 - streak*180);
        lifeTimer = setTimeout(missBird, life);
      }

      startBtn.addEventListener('click', () => {
        playing = true;
        score = 0; streak = 0;
        scoreEl.textContent = 0; streakEl.textContent = 0;
        setMsg("🕊️ Fly, catch, breathe. You've got this!");
        clearTimers();
        spawnBird();
        startBtn.textContent = '↻ Restart';
        stopBtn.disabled = false;
      });

      stopBtn.addEventListener('click', () => {
        playing = false;
        clearTimers();
        if (bird) { bird.remove(); bird = null; }
        setMsg("🌿 Paused. Take a slow breath — press ▶ Start whenever you're ready.");
        startBtn.textContent = '▶ Start';
        stopBtn.disabled = true;
      });
    </script>
    </body>
    </html>
    """
    components.html(game_html, height=560, scrolling=False)
