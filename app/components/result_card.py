import streamlit as st


def render_result(result: dict, input_dict: dict):
    """Render the prediction result card."""

    pred  = result["prediction"]
    prob  = result["probability"]
    pct   = prob * 100

    if pred == 1:
        card_class    = "result-high"
        bar_class     = "bar-high"
        verdict_color = "#e05252"
        icon          = "⚠"
        verdict_text  = "High Risk"
    else:
        card_class    = "result-low"
        bar_class     = "bar-low"
        verdict_color = "#4caf7d"
        icon          = "✓"
        verdict_text  = "Low Risk"

    st.markdown(f"""
    <div class="{card_class}">
      <div style="font-size:2rem; margin-bottom:0.2rem;">{icon}</div>
      <div class="result-verdict" style="color:{verdict_color};">{verdict_text}</div>
      <div class="result-prob"    style="color:{verdict_color};">{pct:.1f}%</div>
      <div class="result-caption">probability of default</div>
      <div class="risk-bar-wrap">
        <div class="{bar_class}" style="width:{min(pct, 100):.1f}%"></div>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:11px; color:#8a8577;">
        <span>0%</span><span>50%</span><span>100%</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Key metrics
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Key Inputs</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-box">
        <div class="val">{int(input_dict['delinquent_months'])}</div>
        <div class="lbl">Delinquent<br>Months</div>
      </div>
      <div class="metric-box">
        <div class="val">{input_dict['credit_utilization_ratio']:.0%}</div>
        <div class="lbl">Credit<br>Utilization</div>
      </div>
      <div class="metric-box">
        <div class="val">{input_dict['avg_dpd_delinquent_ratio']:.0f}</div>
        <div class="lbl">Avg DPD</div>
      </div>
    </div>
    <div class="info-note">
      Model: XGBoost + RandomUnderSampler &nbsp;|&nbsp; Recall: 0.97 &nbsp;|&nbsp; AUC: 0.985
    </div>
    """, unsafe_allow_html=True)


def render_empty_state():
    st.markdown("""
    <div class="empty-state">
      <div style="font-size:2rem; margin-bottom:1rem; opacity:0.4;">🏦</div>
      <div style="color:#8a8577; font-size:14px; line-height:1.7;">
        Fill in the applicant details<br>and click <strong style="color:#c9a84c;">Assess Risk</strong><br>to see the prediction.
      </div>
    </div>
    """, unsafe_allow_html=True)