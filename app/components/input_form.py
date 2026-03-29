import streamlit as st


def render_input_form():
    """Render the applicant input form. Returns (submitted, input_dict)."""

    with st.form("credit_form"):

        # ── Personal Info ──────────────────────────────────────────────────
        st.markdown('<div class="section-label">Personal Information</div>', unsafe_allow_html=True)
        # c1, c2 = st.columns(2)
        # with c1:
        age            = st.number_input("Age", min_value=18, max_value=80, value=35, step=1)
        residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])
        # with c2:
        #     zipcode        = st.number_input("Zipcode", min_value=0, max_value=999999, value=110001, step=1)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Loan Details ───────────────────────────────────────────────────
        st.markdown('<div class="section-label">Loan Details</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            loan_amount        = st.number_input("Loan Amount (₹)", min_value=0, max_value=10_000_000, value=490_000, step=10_000)
            sanction_amount    = st.number_input("Sanction Amount (₹)", min_value=0, max_value=10_000_000, value=500_000, step=10_000)
            loan_tenure_months = st.number_input("Loan Tenure (months)", min_value=1, max_value=360, value=60, step=1)
        with c2:
            loan_purpose = st.selectbox("Loan Purpose", ["Personal", "Auto", "Home", "Education"])
            loan_type    = st.selectbox("Loan Type", ["Secured", "Unsecured"])

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Bureau Data ────────────────────────────────────────────────────
        st.markdown('<div class="section-label">Credit Bureau Data</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            total_loan_months       = st.number_input("Total Loan History (months)", min_value=0, max_value=600, value=120, step=1)
            delinquent_months       = st.number_input("Delinquent Months", min_value=0, max_value=200, value=0, step=1)
            number_of_open_accounts = st.number_input("Open Accounts", min_value=0, max_value=50, value=3, step=1)
        with c2:
            credit_utilization_ratio         = st.slider("Credit Utilization Ratio", 0.0, 1.0, 0.3, step=0.01,
                                                          help="Outstanding credit / Total credit limit")
            delinquent_total_loanmonth_ratio = st.number_input("Delinquent / Total Loan Month Ratio (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1,
                                                                help="(Delinquent Months / Total Loan Months) × 100")
            avg_dpd_delinquent_ratio         = st.number_input("Avg DPD per Delinquent Month", min_value=0.0, max_value=1000.0, value=0.0, step=1.0,
                                                                help="Total DPD / Delinquent Months (0 if no delinquency)")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("→  Assess Risk")

    # Derive loan_to_income_ratio — income was dropped from model but ratio was kept
    # We set it 0 since income is unavailable; scaler dummy row handles the rest
    loan_to_income_ratio = 0.0

    # gst and net_disbursement are in the scaler but dropped from final model
    # predictor fills them as 0 in the dummy row automatically
    input_dict = {
        "age":                              age,
        "zipcode":                          0,
        "sanction_amount":                  sanction_amount,
        "loan_amount":                      loan_amount,
        "loan_tenure_months":               loan_tenure_months,
        "number_of_open_accounts":          number_of_open_accounts,
        "total_loan_months":                total_loan_months,
        "delinquent_months":                delinquent_months,
        "credit_utilization_ratio":         credit_utilization_ratio,
        "loan_to_income_ratio":             loan_to_income_ratio,
        "delinquent_total_loanmonth_ratio": delinquent_total_loanmonth_ratio,
        "avg_dpd_delinquent_ratio":         avg_dpd_delinquent_ratio,
        # Categorical
        "residence_type":                   residence_type,
        "loan_purpose":                     loan_purpose,
        "loan_type":                        loan_type,
    }

    return submitted, input_dict