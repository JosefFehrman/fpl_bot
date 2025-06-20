import streamlit as st
import sidebar
from views import home, stats, predictions, train, data

st.set_page_config(page_title="Fantasy Fehrman Premier League AI Bot", layout="wide")
page = sidebar.render_sidebar()

if page == "Home":
    home.render()
elif page == "Stats":
    stats.render()
elif page == "Predictions":
    predictions.render()
elif page == "Train":
    train.render()
elif page == "Data":
    data.render()