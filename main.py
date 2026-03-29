import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Risk Model",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0f1117;
    color: #e8e8e8;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #161b27;
    border-right: 1px solid #2a2f3e;
}

/* Header */
.main-header {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #f0f0f0;
    letter-spacing: -0.5px;
    margin-bottom: 0.2rem;
}
.sub-header {
    color: #6b7280;
    font-size: 0.95rem;
    font-weight: 300;
    margin-bottom: 2rem;
}

/* Cards */
.metric-card {
    background: #161b27;
    border: 1px solid #2a2f3e;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.metric-label {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 600;
    color: #f0f0f0;
}

/* Result cards */
.result-default {
    background: linear-gradient(135deg, #2d1b1b, #1a0f0f);
    border: 1px solid #ef4444;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}
.result-no-default {
    background: linear-gradient(135deg, #1b2d1b, #0f1a0f);
    border: 1px solid #22c55e;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}
.result-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}
.result-subtitle {
    font-size: 0.9rem;
    color: #9ca3af;
}

/* Section titles */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #f0f0f0;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #2a2f3e;
}

/* Input styling */
.stSelectbox label, .stNumberInput label, .stSlider label {
    color: #9ca3af !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    transform: translateY(-1px);
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #161b27;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #6b7280;
    border-radius: 6px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #2a2f3e !important;
    color: #f0f0f0 !important;
}

/* Divider */
hr { border-color: #2a2f3e; }

/* Warning/info boxes */
.stAlert { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    """Load model from artifacts folder"""
    model_path = Path('artifacts/model_data.joblib')


    if model_path.exists():
        return joblib.load(model_path)
    return None


model_data = load_model()


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
# def prepare_input(inputs: dict, model_data: dict) -> pd.DataFrame:
#     """Prepare input dataframe matching training features"""
#
#     # One-hot encode categorical features manually
#     df = pd.DataFrame([{
#         'age': inputs['age'],
#         'sanction_amount': inputs['sanction_amount'],
#         'loan_tenure_months': inputs['loan_tenure_months'],
#         'number_of_open_accounts': inputs['number_of_open_accounts'],
#         'total_loan_months': inputs['total_loan_months'],
#         'delinquent_months': inputs['delinquent_months'],
#         'credit_utilization_ratio': inputs['credit_utilization_ratio'],
#         'loan_to_income_ratio': inputs['loan_to_income_ratio'],
#         'delinquent_total_loanmonth_ratio': inputs['delinquent_total_loanmonth_ratio'],
#         'avg_dpd_delinquent_ratio': inputs['avg_dpd_delinquent_ratio'],
#         # Residence type
#         'residence_type_Owned': 1 if inputs['residence_type'] == 'Owned' else 0,
#         'residence_type_Rented': 1 if inputs['residence_type'] == 'Rented' else 0,
#         # Loan purpose
#         'loan_purpose_Education': 1 if inputs['loan_purpose'] == 'Education' else 0,
#         'loan_purpose_Home': 1 if inputs['loan_purpose'] == 'Home' else 0,
#         'loan_purpose_Personal': 1 if inputs['loan_purpose'] == 'Personal' else 0,
#         # Loan type
#         'loan_type_Unsecured': 1 if inputs['loan_type'] == 'Unsecured' else 0,
#     }])
#
#     # Scale numerical columns
#     if model_data:
#         scaler = model_data['scaler']
#         cols_to_scale = [c for c in model_data['cols_to_scale'] if c in df.columns]
#         df[cols_to_scale] = scaler.transform(df[cols_to_scale])
#
#     return df
# def prepare_input(inputs: dict, model_data: dict) -> pd.DataFrame:
#     df = pd.DataFrame([{...}])  # your existing code
#
#     # DEBUG — add these lines
#     print("DataFrame columns:", df.columns.tolist())
#     print("Expected features:", list(model_data['features']))
#     print("DataFrame shape:", df.shape)
#
#
#
#     # Fix 1 — ensure correct column order matching training
#     feature_cols = model_data['features']
#     df = df[feature_cols]
#
#     # Fix 2 — convert all columns to float
#     df = df.astype(float)  # ← this fixes the error
#
#     # Only scale columns that exist in BOTH df and cols_to_scale
#     cols_to_scale = [c for c in model_data['cols_to_scale']
#                      if c in df.columns]  # ← this line fixes it
#
#     if cols_to_scale:
#         df[cols_to_scale] = model_data['scaler'].transform(df[cols_to_scale])
#
#     # Add this before prediction
#     print(input_df.dtypes)
#     print(input_df.shape)
#
#     return df
def prepare_input(inputs: dict, model_data: dict) -> pd.DataFrame:
    row = {
        'age': float(inputs['age']),
        'sanction_amount': float(inputs['sanction_amount']),
        'loan_tenure_months': float(inputs['loan_tenure_months']),
        'number_of_open_accounts': float(inputs['number_of_open_accounts']),
        'total_loan_months': float(inputs['total_loan_months']),
        'delinquent_months': float(inputs['delinquent_months']),
        'credit_utilization_ratio': float(inputs['credit_utilization_ratio']),
        'loan_to_income_ratio': float(inputs['loan_to_income_ratio']),
        'delinquent_total_loanmonth_ratio': float(inputs['delinquent_total_loanmonth_ratio']),
        'avg_dpd_delinquent_ratio': float(inputs['avg_dpd_delinquent_ratio']),
        'residence_type_Owned': 1.0 if inputs['residence_type'] == 'Owned' else 0.0,
        'residence_type_Rented': 1.0 if inputs['residence_type'] == 'Rented' else 0.0,
        'loan_purpose_Education': 1.0 if inputs['loan_purpose'] == 'Education' else 0.0,
        'loan_purpose_Home': 1.0 if inputs['loan_purpose'] == 'Home' else 0.0,
        'loan_purpose_Personal': 1.0 if inputs['loan_purpose'] == 'Personal' else 0.0,
        'loan_type_Unsecured': 1.0 if inputs['loan_type'] == 'Unsecured' else 0.0,
    }

    # Build with explicit float types from start
    df = pd.DataFrame([row])

    # Verify columns match
    feature_cols = list(model_data['features'])
    missing = set(feature_cols) - set(df.columns)
    extra = set(df.columns) - set(feature_cols)

    print("Missing from input:", missing)
    print("Extra in input:", extra)

    # Reorder to match training
    df = df[feature_cols]

    # Scale
    cols_to_scale = [c for c in model_data['cols_to_scale']
                     if c in df.columns]
    if cols_to_scale:
        df[cols_to_scale] = model_data['scaler'].transform(df[cols_to_scale])

    return df



def get_feature_importance(model_data: dict) -> pd.DataFrame:
    """Extract feature importance from model"""
    model = model_data['model']
    features = list(model_data['features'])

    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importance = np.abs(model.coef_[0])
    else:
        return None

    df = pd.DataFrame({
        'Feature': features,
        'Importance': importance
    }).sort_values('Importance', ascending=True).tail(15)

    return df


# ─────────────────────────────────────────────
# SIDEBAR — NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0;'>
        <div style='font-family: DM Serif Display, serif; font-size: 1.4rem; color: #f0f0f0;'>
            🏦 CreditRisk
        </div>
        <div style='font-size: 0.75rem; color: #6b7280; margin-top: 0.3rem;'>
            ML Classification Model
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigation",
        ["🔍 Predict", "📊 Model Performance", "📈 Feature Importance"],
        label_visibility="collapsed"
    )

    st.divider()

    # Model status
    if model_data:
        st.success("✅ Model loaded successfully")
    else:
        st.warning("⚠️ Model not found\nPlace model_data.joblib in ../artifacts/")

    st.markdown("""
    <div style='position: fixed; bottom: 1rem; font-size: 0.72rem; color: #4b5563;'>
        Credit Risk Classification v1.0
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE 1 — PREDICT
# ─────────────────────────────────────────────
if "Predict" in page:

    st.markdown('<div class="main-header">Credit Risk Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enter customer details to predict default risk</div>', unsafe_allow_html=True)

    with st.form("prediction_form"):

        # ── Customer & Loan Info ──
        st.markdown('<div class="section-title">Customer Information</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.number_input("Age", min_value=18, max_value=80, value=35)
            residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])
        with col2:
            sanction_amount = st.number_input("Sanction Amount (₹)", min_value=10000, max_value=10000000, value=500000,
                                              step=10000)
            loan_purpose = st.selectbox("Loan Purpose", ["Personal", "Home", "Education", "Auto"])
        with col3:
            loan_tenure_months = st.number_input("Loan Tenure (Months)", min_value=6, max_value=360, value=36)
            loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])

        # ── Financial Info ──
        st.markdown('<div class="section-title">Financial Information</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=1000, max_value=10000000, value=50000, step=1000)
            number_of_open_accounts = st.number_input("Open Accounts", min_value=0, max_value=50, value=2)
        with col2:
            credit_utilization_ratio = st.slider("Credit Utilization Ratio (%)", 0, 100, 30)
            total_loan_months = st.number_input("Total Loan Months", min_value=0, max_value=360, value=24)
        with col3:
            loan_to_income_ratio = st.number_input("Loan to Income Ratio", min_value=0.0, max_value=100.0,
                                                   value=round(sanction_amount / max(income, 1), 2), format="%.2f")

        # ── Bureau Info ──
        st.markdown('<div class="section-title">Bureau Information</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            delinquent_months = st.number_input("Delinquent Months", min_value=0, max_value=120, value=0)
        with col2:
            avg_dpd_delinquent_ratio = st.number_input("Avg DPD / Delinquent Ratio", min_value=0.0, value=0.0,
                                                       format="%.2f")
        with col3:
            delinquent_total_loanmonth_ratio = st.number_input("Delinquent / Total Loan Month Ratio", min_value=0.0,
                                                               max_value=1.0, value=0.0, format="%.3f")

        submitted = st.form_submit_button("🔍 Predict Default Risk")

    # ── Prediction Result ──
    if submitted:
        inputs = {
            'age': age,
            'sanction_amount': sanction_amount,
            'loan_tenure_months': loan_tenure_months,
            'number_of_open_accounts': number_of_open_accounts,
            'total_loan_months': total_loan_months,
            'delinquent_months': delinquent_months,
            'credit_utilization_ratio': credit_utilization_ratio,
            'loan_to_income_ratio': loan_to_income_ratio,
            'delinquent_total_loanmonth_ratio': delinquent_total_loanmonth_ratio,
            'avg_dpd_delinquent_ratio': avg_dpd_delinquent_ratio,
            'residence_type': residence_type,
            'loan_purpose': loan_purpose,
            'loan_type': loan_type,
        }

        if model_data:
            input_df = prepare_input(inputs, model_data)
            prediction = model_data['model'].predict(input_df)[0]
            probability = model_data['model'].predict_proba(input_df)[0]
            default_prob = probability[1] * 100

            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                if prediction:
                    st.markdown(f"""
                    <div class="result-default">
                        <div class="result-title" style="color: #ef4444;">⚠️ Default Risk</div>
                        <div style="font-size: 3rem; font-weight: 700; color: #ef4444; margin: 0.5rem 0;">
                            {default_prob:.1f}%
                        </div>
                        <div class="result-subtitle">High probability of loan default</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-no-default">
                        <div class="result-title" style="color: #22c55e;">✅ No Default</div>
                        <div style="font-size: 3rem; font-weight: 700; color: #22c55e; margin: 0.5rem 0;">
                            {100 - default_prob:.1f}%
                        </div>
                        <div class="result-subtitle">Low probability of loan default</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Key metrics
            st.markdown("---")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">Default Probability</div><div class="metric-value">{default_prob:.1f}%</div></div>',
                    unsafe_allow_html=True)
            with c2:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">Loan to Income</div><div class="metric-value">{loan_to_income_ratio:.2f}x</div></div>',
                    unsafe_allow_html=True)
            with c3:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">Delinquent Months</div><div class="metric-value">{delinquent_months}</div></div>',
                    unsafe_allow_html=True)
            with c4:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">Credit Utilization</div><div class="metric-value">{credit_utilization_ratio}%</div></div>',
                    unsafe_allow_html=True)
        else:
            st.error("Model not loaded. Please check that model_data.joblib exists in the artifacts folder.")


# ─────────────────────────────────────────────
# PAGE 2 — MODEL PERFORMANCE
# ─────────────────────────────────────────────
elif "Performance" in page:

    st.markdown('<div class="main-header">Model Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluation metrics on test set (12,498 samples)</div>', unsafe_allow_html=True)

    # Hardcoded from your classification report
    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("Accuracy", "93%", "#3b82f6"),
        ("Recall (Default)", "96%", "#22c55e"),
        ("Precision (Default)", "55%", "#f59e0b"),
        ("F1 Score (Default)", "70%", "#8b5cf6"),
    ]

    for col, (label, value, color) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-color: {color}33;">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color: {color};">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Classification Report</div>', unsafe_allow_html=True)

        report_data = {
            'Class': ['Non-Default (0)', 'Default (1)', 'Macro Avg', 'Weighted Avg'],
            'Precision': [1.00, 0.55, 0.77, 0.96],
            'Recall': [0.93, 0.96, 0.95, 0.93],
            'F1-Score': [0.96, 0.70, 0.83, 0.94],
            'Support': [11424, 1074, 12498, 12498]
        }

        df_report = pd.DataFrame(report_data)
        st.dataframe(
            df_report.style.format({
                'Precision': '{:.2f}',
                'Recall': '{:.2f}',
                'F1-Score': '{:.2f}',
            }).background_gradient(subset=['Precision', 'Recall', 'F1-Score'], cmap='Blues'),
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.markdown('<div class="section-title">Class Distribution (Test Set)</div>', unsafe_allow_html=True)

        fig = go.Figure(data=[
            go.Bar(
                x=['Non-Default', 'Default'],
                y=[11424, 1074],
                marker_color=['#3b82f6', '#ef4444'],
                text=[11424, 1074],
                textposition='outside',
                textfont=dict(color='#e8e8e8')
            )
        ])
        fig.update_layout(
            paper_bgcolor='#161b27',
            plot_bgcolor='#161b27',
            font=dict(color='#e8e8e8'),
            showlegend=False,
            margin=dict(t=20, b=20),
            yaxis=dict(gridcolor='#2a2f3e'),
            xaxis=dict(gridcolor='#2a2f3e'),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Confusion Matrix
    st.markdown('<div class="section-title">Confusion Matrix</div>', unsafe_allow_html=True)

    # Calculated from report: recall 0.93 for class 0 → TP=10624, FN=800; recall 0.96 for class 1 → TP=1031, FN=43
    cm = np.array([[10624, 800], [43, 1031]])

    fig_cm = px.imshow(
        cm,
        labels=dict(x="Predicted", y="Actual", color="Count"),
        x=['Non-Default', 'Default'],
        y=['Non-Default', 'Default'],
        color_continuous_scale='Blues',
        text_auto=True
    )
    fig_cm.update_layout(
        paper_bgcolor='#161b27',
        plot_bgcolor='#161b27',
        font=dict(color='#e8e8e8'),
        margin=dict(t=20, b=20),
        width=500
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.plotly_chart(fig_cm, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE 3 — FEATURE IMPORTANCE
# ─────────────────────────────────────────────
elif "Feature" in page:

    st.markdown('<div class="main-header">Feature Importance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Which features drive the model predictions most</div>', unsafe_allow_html=True)

    if model_data:
        fi_df = get_feature_importance(model_data)

        if fi_df is not None:
            fig = go.Figure(go.Bar(
                x=fi_df['Importance'],
                y=fi_df['Feature'],
                orientation='h',
                marker=dict(
                    color=fi_df['Importance'],
                    colorscale='Blues',
                    showscale=False
                ),
                text=fi_df['Importance'].round(4),
                textposition='outside',
                textfont=dict(color='#e8e8e8', size=11)
            ))
            fig.update_layout(
                paper_bgcolor='#161b27',
                plot_bgcolor='#161b27',
                font=dict(color='#e8e8e8', family='DM Sans'),
                height=550,
                margin=dict(l=20, r=80, t=20, b=20),
                xaxis=dict(gridcolor='#2a2f3e', title='Importance Score'),
                yaxis=dict(gridcolor='#2a2f3e'),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Key insight
            top_feature = fi_df.iloc[-1]['Feature']
            st.info(
                f"💡 **Top predictor:** `{top_feature}` has the highest influence on default prediction in your model.")
        else:
            st.warning("Feature importance not available for this model type.")
    else:
        # Show placeholder with known important features from your analysis
        st.markdown('<div class="section-title">Expected Feature Importance (Based on IV Analysis)</div>',
                    unsafe_allow_html=True)

        placeholder_data = pd.DataFrame({
            'Feature': ['avg_dpd_delinquent_ratio', 'delinquent_months', 'delinquent_total_loanmonth_ratio',
                        'credit_utilization_ratio', 'loan_to_income_ratio', 'repayment_progress',
                        'enquiry_count', 'sanction_amount', 'loan_tenure_months', 'age'],
            'IV Score': [0.45, 0.40, 0.35, 0.28, 0.22, 0.18, 0.15, 0.12, 0.10, 0.08]
        })

        fig = go.Figure(go.Bar(
            x=placeholder_data['IV Score'],
            y=placeholder_data['Feature'],
            orientation='h',
            marker_color='#3b82f6',
            text=placeholder_data['IV Score'],
            textposition='outside',
            textfont=dict(color='#e8e8e8')
        ))
        fig.update_layout(
            paper_bgcolor='#161b27',
            plot_bgcolor='#161b27',
            font=dict(color='#e8e8e8'),
            height=450,
            margin=dict(l=20, r=60, t=20, b=20),
            xaxis=dict(gridcolor='#2a2f3e', title='IV Score'),
            yaxis=dict(gridcolor='#2a2f3e'),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.warning(
            "⚠️ Model not loaded — showing IV-based importance from your analysis. Load model for actual feature importance.")