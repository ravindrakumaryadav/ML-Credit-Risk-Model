import streamlit as st
from joblib import load
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../artifacts/model_data.joblib")


@st.cache_resource
def load_model():
    """Load and cache the model artifacts from joblib."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at: {MODEL_PATH}\n"
            "Run the export script in the notebook first."
        )
    return load(MODEL_PATH)