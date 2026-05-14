import streamlit as st
import plotly.express as px


def render_heatmap(df):

    st.subheader("🌡️ Heatmap Estratégico")

    columnas = [
        "FINANZAS",
        "COMERCIAL",
        "OPERACIONES",
        "FORMACION",
        "SOSTENIBILIDAD",
        "SCORE_TOTAL",
        "ESG_SCORE"
    ]

    corr = df[columnas].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdYlGn",
        aspect="auto"
    )

    fig.update_layout(
        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "El mapa de calor detecta correlaciones estratégicas."
    )