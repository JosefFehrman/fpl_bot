import streamlit as st
from streamlit_app import sidebar
from streamlit_app.views import home, stats, predictions

st.set_page_config(page_title="Fantasy Fehrman Premier League AI Bot", layout="wide")
page = sidebar.render_sidebar()

if page == "Home":
    home.render()
elif page == "Stats":
    stats.render()
elif page == "Predictions":
    predictions.render()