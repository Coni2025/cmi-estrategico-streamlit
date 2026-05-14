import streamlit as st


def render_dashboard(df):

    st.subheader("📊 Dashboard Ejecutivo")

    st.dataframe(
        df,
        use_container_width=True,
        height=600
    )