import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0f0f13; color: #e8e4dc; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 3rem 3rem; max-width: 1100px; }

/* Hero */
.hero { border-bottom: 1px solid #2a2a35; padding-bottom: 2rem; margin-bottom: 2.5rem; }
.hero-eyebrow { font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: #c9a84c; font-weight: 500; margin-bottom: 0.5rem; }
.hero-title { font-family: 'DM Serif Display', serif; font-size: 3rem; line-height: 1.05; color: #f0ece3; margin: 0 0 0.6rem 0; }
.hero-title em { font-style: italic; color: #c9a84c; }
.hero-sub { font-size: 15px; color: #8a8577; font-weight: 300; line-height: 1.6; }

/* Section label */
.section-label { font-size: 10px; letter-spacing: 0.2em; text-transform: uppercase; color: #c9a84c; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 8px; }
.section-label::after { content: ''; flex: 1; height: 1px; background: #2a2a35; }

/* Inputs */
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] > div > div {
    background: #1e1e28 !important; border: 1px solid #2a2a35 !important;
    border-radius: 8px !important; color: #e8e4dc !important;
}
label { color: #9e9a91 !important; font-size: 13px !important; font-weight: 400 !important; }

/* Button */
div[data-testid="stFormSubmitButton"] > button {
    background: #c9a84c !important; color: #0f0f13 !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 14px !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
    padding: 0.7rem 2rem !important; width: 100% !important;
}
div[data-testid="stFormSubmitButton"] > button:hover { opacity: 0.88 !important; }

/* Result */
.result-high { background: linear-gradient(135deg,#2a1010,#1e1010); border: 1px solid #5c1a1a; border-radius: 16px; padding: 2rem; text-align: center; }
.result-low  { background: linear-gradient(135deg,#0f2a1a,#0a1e12); border: 1px solid #1a5c2a; border-radius: 16px; padding: 2rem; text-align: center; }
.result-verdict { font-family: 'DM Serif Display', serif; font-size: 2rem; margin: 0.3rem 0 0.5rem 0; }
.result-prob    { font-size: 3.5rem; font-weight: 600; line-height: 1; margin: 0.5rem 0; }
.result-caption { font-size: 13px; color: #8a8577; font-weight: 300; }

/* Risk bar */
.risk-bar-wrap { background: #1e1e28; border-radius: 4px; height: 6px; margin: 1rem 0 0.4rem 0; overflow: hidden; }
.bar-high { height:100%; border-radius:4px; background: linear-gradient(90deg,#c9a84c,#e05252); }
.bar-low  { height:100%; border-radius:4px; background: linear-gradient(90deg,#c9a84c,#4caf7d); }

/* Metrics */
.metric-row { display:flex; gap:1rem; margin-top:1.2rem; }
.metric-box { flex:1; background:#1e1e28; border:1px solid #2a2a35; border-radius:8px; padding:0.8rem 1rem; text-align:center; }
.metric-box .val { font-size:1.4rem; font-weight:600; color:#c9a84c; }
.metric-box .lbl { font-size:11px; color:#8a8577; text-transform:uppercase; letter-spacing:0.1em; margin-top:2px; }

/* Empty state */
.empty-state { border:1px dashed #2a2a35; border-radius:12px; padding:3rem 2rem; text-align:center; margin-top:1rem; }

/* Info note */
.info-note { background:#1a1a24; border-left:3px solid #c9a84c; border-radius:0 6px 6px 0; padding:0.6rem 1rem; font-size:12px; color:#8a8577; margin-top:1rem; line-height:1.6; }
</style>
"""


def apply_styles():
    st.markdown(CSS, unsafe_allow_html=True)