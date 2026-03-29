import streamlit as st


def render_header():
    st.markdown("""
    <div class="hero">
      <div class="hero-eyebrow">AI-Powered Assessment</div>
      <h1 class="hero-title">Credit <em>Risk</em> Predictor</h1>
      <p class="hero-sub">Enter applicant details to assess default probability using XGBoost trained on bureau and loan data.</p>
    </div>
    """, unsafe_allow_html=True)