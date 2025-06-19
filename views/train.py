import streamlit as st
from src.model import train_model

def render():
    st.subheader("🤖 Train Weekly Score Model")

    if st.button("Train Model"):
        results_df = train_model()
        st.success("✅ Model trained and saved.")

        st.subheader("📊 Model Evaluation Results")
        st.dataframe(results_df)

        best = results_df.sort_values("R²", ascending=False).iloc[0]
        st.info(f"🏆 Best model: {best['Model']} (R² = {best['R²']})")

