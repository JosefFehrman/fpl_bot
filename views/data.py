import streamlit as st
from src.data_fetcher import fetch_weekly_data

def render():
    st.subheader("📦 Update Gameweek Data")
    if st.button("Fetch Weekly Player History"):
        df = fetch_weekly_data()
        st.success(f"Downloaded {len(df)} rows of data")
        st.dataframe(df.head())
