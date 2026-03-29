# ML-Credit-Risk-Model
End-to-end credit risk classification model using XGBoost with 98.4% AUC-ROC, built on 50K loan records with feature engineering, VIF analysis, and WoE/IV-based feature selection.

# Credit Risk Model

An end-to-end machine learning project to predict the probability of loan default using customer, loan, and credit bureau data. Includes a full ML pipeline in a Jupyter notebook and a structured Streamlit web application for real-time inference.

---

## Project Structure

```
Credit-Risk-Model/
├── app/                        # Streamlit web application
│   ├── main.py                 # Entry point
│   ├── pages/
│   │   └── predict.py          # Prediction page
│   ├── components/
│   │   ├── header.py           # Page header
│   │   ├── input_form.py       # Applicant input form
│   │   └── result_card.py      # Prediction result display
│   └── utils/
│       ├── model_loader.py     # Loads and caches the joblib artifact
│       ├── predictor.py        # Prediction logic (isolated from UI)
│       └── ui.py               # Global CSS styles
├── artifacts/
│   └── model_data.joblib       # Saved model, scaler, and feature metadata
├── dataset/
│   ├── customers.csv           # Customer personal information
│   ├── loans.csv               # Loan details
│   └── bureau_data.csv         # Credit bureau data
├── documents/                  # Project documentation
├── notebook/
│   └── Credit_Risk_Model.ipynb # Full ML pipeline notebook
├── sow/                        # Scope of work
├── requirements.txt
└── README.md
```

---

## Problem Statement

Predict whether a loan applicant will default, using a dataset of 50,000 records across three sources — customer profiles, loan details, and credit bureau history. The dataset is heavily imbalanced (~91% non-default, ~8% default), making recall on the default class the primary metric.

**Target:** `default` (1 = defaulted, 0 = did not default)

---

## ML Pipeline

### 1. Data Ingestion
Three CSV files merged on `cust_id`: `customers.csv`, `loans.csv`, `bureau_data.csv`.

### 2. Data Leakage Prevention
Train/test split (75/25, stratified) performed **before** any EDA or feature engineering to prevent contamination.

### 3. Data Cleaning
- `residence_type` null values filled with mode
- Typo corrected: `"Personaal"` → `"Personal"` in `loan_purpose`
- Rows with `income = 0` removed
- ID columns (`cust_id`, `loan_id`) and date columns dropped

### 4. Feature Engineering
| Feature | Formula |
|---|---|
| `loan_to_income_ratio` | `(loan_amount / income) × 100` |
| `delinquent_total_loanmonth_ratio` | `(delinquent_months / total_loan_months) × 100` |
| `avg_dpd_delinquent_ratio` | `total_dpd / delinquent_months` (0 if no delinquency) |
| `repayment_progress` | `1 - (principal_outstanding / sanction_amount)` |

### 5. Multicollinearity — VIF (Variance Inflation Factor)
Iterative VIF analysis, dropping one feature at a time:
- **Iteration 1:** Dropped `total_dpd` (VIF = 51.29)
- **Iteration 2:** Dropped `income` (high VIF, correlated with `bank_balance_at_application`)
- **Iteration 3:** Replaced `principal_outstanding` with `repayment_progress` ratio
- **Iteration 4:** Reviewed `loan_tenure_months` vs `total_loan_months`

### 6. Feature Selection — WoE / IV (Information Value)
Weight of Evidence and Information Value computed for all features.

Dropped (IV < 0.02 — no predictive power):
- **Categorical:** `gender`, `marital_status`, `employment_status`, `city`, `state`
- **Numeric:** `enquiry_count`, `bank_balance_at_application`, `years_at_current_address`, `number_of_dependants`, `repayment_progress`, `number_of_closed_accounts`

### 7. Scaling & Encoding
- `MinMaxScaler` fitted on train set only, applied to both train and test
- `pd.get_dummies(drop_first=True)` for one-hot encoding

### 8. Class Imbalance Handling
Techniques evaluated:
- `RandomUnderSampler` (RUS)
- `SMOTETomek`

### 9. Models Trained

| Model | Recall (Class 1) | Precision (Class 1) | AUC-ROC |
|---|---|---|---|
| Logistic Regression (base) | 0.72 | 0.85 | — |
| Random Forest (base) | 0.69 | 0.87 | — |
| XGBoost (base) | 0.75 | 0.82 | — |
| RandomizedSearchCV + LR | 0.95 | 0.54 | — |
| LR + RUS | 0.96 | 0.51 | — |
| **XGBoost + RUS** ✅ | **0.97** | **0.55** | **0.985** |
| LR + SMOTETomek | 0.94 | 0.56 | — |
| XGBoost + SMOTETomek | 0.81 | 0.76 | — |
| Optuna + XGBoost | 0.85 | 0.71 | — |

### 10. Final Model
**XGBoost + RandomUnderSampler**
- Recall: **0.97** — catches 97% of actual defaulters
- AUC-ROC: **0.985**
- Gini Coefficient: **0.97**
- KS Statistic computed via decile analysis

---

## Evaluation Metrics

| Metric | Value |
|---|---|
| Recall (Class 1) | 0.97 |
| Precision (Class 1) | 0.55 |
| AUC-ROC | 0.985 |
| Gini Coefficient | 0.97 |

> Recall is prioritised over precision — missing a defaulter is more costly than a false alarm.

---

## Web Application

Built with Streamlit. Structured as a modular application with separated concerns across pages, components, and utilities.

### Run locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate the model artifact (run from notebook/ directory)
#    Execute all cells in Credit_Risk_Model.ipynb

# 3. Launch the app (run from app/ directory)
cd app
streamlit run main.py
```

### Input Features

| Feature | Description |
|---|---|
| Age | Applicant age |
| Residence Type | Owned / Rented / Mortgage |
| Loan Amount | Amount sanctioned (₹) |
| Sanction Amount | Total sanctioned limit (₹) |
| Loan Tenure | Duration in months |
| Loan Purpose | Personal / Auto / Home / Education |
| Loan Type | Secured / Unsecured |
| Total Loan History | Total months of loan history |
| Delinquent Months | Months with missed payments |
| Open Accounts | Number of active loan accounts |
| Credit Utilization Ratio | Outstanding / Total credit limit |
| Delinquent/Total Loan Month Ratio | Delinquency rate over loan history |
| Avg DPD per Delinquent Month | Average days past due |

---

## Tech Stack

| Layer | Library |
|---|---|
| Data processing | `pandas`, `numpy` |
| Visualisation | `matplotlib`, `seaborn` |
| ML models | `scikit-learn`, `xgboost` |
| Imbalance handling | `imbalanced-learn` |
| Hyperparameter tuning | `optuna` |
| Model serialisation | `joblib` |
| Web application | `streamlit` |

---

## Key Findings

- **Credit utilization ratio** is the strongest predictor (IV = 2.35)
- **Delinquent months** and **avg DPD** are the next most important bureau features
- Demographic features (gender, marital status, employment status) showed near-zero IV and were dropped
- Class imbalance required explicit handling — base models missed 25–30% of defaulters
- RandomUnderSampler outperformed SMOTETomek for recall on this dataset