import streamlit as st
import plotly.express as px


def render_clustering(df):

    st.subheader("🌐 Clustering Empresarial")

    fig = px.scatter(

        df,

        x="X",

        y="Y",

        color=df["CLUSTER"].astype(str),

        hover_name="EMPRESA",

        size="SCORE_TOTAL",

        color_discrete_sequence=[
            "#2563eb",
            "#dc2626",
            "#16a34a"
        ]
    )

    fig.update_layout(

        height=700,

        xaxis_title="Componente PCA 1",

        yaxis_title="Componente PCA 2",

        legend_title="Cluster"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "La IA agrupa empresas según patrones estratégicos similares."
    )