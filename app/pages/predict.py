import streamlit as st
from utils.model_loader import load_model
from utils.predictor import predict
from components.input_form import render_input_form
from components.result_card import render_result, render_empty_state


def render_predict_page():

    # Load model — show error clearly if missing
    try:
        model_data = load_model()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    col_form, _, col_result = st.columns([5, 0.3, 3])

    with col_form:
        submitted, input_dict = render_input_form()

    with col_result:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if submitted:
            result = predict(input_dict, model_data)
            render_result(result, input_dict)
        else:
            render_empty_state()