import streamlit as st

def render_sidebar():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ["Home", "Stats", "Predictions", "Train", "Data"])
    return page
