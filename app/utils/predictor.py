import pandas as pd
import numpy as np

SCALER_COLS = [
    'age', 'income', 'number_of_dependants', 'years_at_current_address',
    'zipcode', 'sanction_amount', 'loan_amount', 'processing_fee', 'gst',
    'net_disbursement', 'loan_tenure_months', 'principal_outstanding',
    'bank_balance_at_application', 'number_of_open_accounts',
    'number_of_closed_accounts', 'total_loan_months', 'delinquent_months',
    'total_dpd', 'enquiry_count', 'credit_utilization_ratio',
    'loan_to_income_ratio', 'delinquent_total_loanmonth_ratio',
    'avg_dpd_delinquent_ratio',
]

FINAL_NUMERIC_COLS = [
    'age', 'zipcode', 'sanction_amount', 'loan_amount', 'processing_fee',
    'gst', 'net_disbursement', 'loan_tenure_months', 'number_of_open_accounts',
    'total_loan_months', 'delinquent_months', 'credit_utilization_ratio',
    'loan_to_income_ratio', 'delinquent_total_loanmonth_ratio',
    'avg_dpd_delinquent_ratio',
]


def predict(input_dict: dict, model_data: dict) -> dict:
    model    = model_data["model"]
    scaler   = model_data["scaler"]
    features = model_data["features"]

    # Step 1: full dummy row with all 23 scaler columns set to 0
    dummy_row = pd.DataFrame(0.0, index=[0], columns=SCALER_COLS)

    # Step 2: fill in values we have from the form
    for col in SCALER_COLS:
        if col in input_dict:
            dummy_row[col] = input_dict[col]



    # Step 3: scale — scaler now gets all 23 columns it expects
    scaled_df = pd.DataFrame(
        scaler.transform(dummy_row), columns=SCALER_COLS
    )

    # Step 4: keep only the 15 final numeric columns
    df = scaled_df[FINAL_NUMERIC_COLS].copy()

    # Step 5: add categoricals back
    for col in ['residence_type', 'loan_purpose', 'loan_type']:
        df[col] = input_dict[col]

    # Step 6: encode and align to model features
    df_encoded = pd.get_dummies(df, drop_first=True)
    df_encoded = df_encoded.reindex(columns=features, fill_value=0)

    prob = float(model.predict_proba(df_encoded)[0][1])
    pred = int(model.predict(df_encoded)[0])

    return {
        "prediction":  pred,
        "probability": round(prob, 4),
        "risk_label":  "High Risk" if pred == 1 else "Low Risk",
    }