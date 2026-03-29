import streamlit as st
from utils.ui import apply_styles
from components.header import render_header
from pages.predict import render_predict_page

st.set_page_config(
    page_title="Credit Risk Predictor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_styles()
render_header()
render_predict_page()