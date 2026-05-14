import streamlit as st
import plotly.express as px

# =====================================================
# STRATEGIC MAP
# =====================================================

def render_strategic_map(df):

    st.subheader("🗺️ Strategic Corporate Map AI")

    # =====================================================
    # FILTROS
    # =====================================================

    sectores = ["TODOS"] + sorted(
        df["SECTOR"].unique().tolist()
    )

    sector = st.selectbox(
        "Filtrar sector",
        sectores
    )

    if sector != "TODOS":

        df = df[
            df["SECTOR"] == sector
        ]

    # =====================================================
    # MAPA
    # =====================================================

    fig = px.scatter(

        df,

        x="X",
        y="Y",

        size="SCORE_TOTAL",

        color="ESG_SCORE",

        hover_name="EMPRESA",

        hover_data=[
            "SECTOR",
            "SCORE_TOTAL",
            "CLASIFICACION",
            "CLUSTER"
        ],

        color_continuous_scale="RdYlGn",

        size_max=45
    )

    # =====================================================
    # ESTILO
    # =====================================================

    fig.update_traces(

        marker=dict(
            line=dict(
                width=2,
                color="white"
            ),
            opacity=0.85
        )
    )

    fig.update_layout(

        height=750,

        plot_bgcolor="#f8fafc",

        paper_bgcolor="#f8fafc",

        title="Mapa Estratégico Corporativo IA",

        font=dict(
            size=14
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # IA ANALISIS
    # =====================================================

    top = df.sort_values(
        by="SCORE_TOTAL",
        ascending=False
    ).iloc[0]

    riesgo = df.sort_values(
        by="ESG_SCORE",
        ascending=True
    ).iloc[0]

    disruptiva = df.loc[
        df["X"].abs().idxmax()
    ]

    st.success(
        f"🏆 Líder estratégico detectado: {top['EMPRESA']}"
    )

    st.warning(
        f"⚠️ Riesgo ESG detectado: {riesgo['EMPRESA']}"
    )

    st.info(
        f"🧠 Empresa disruptiva IA: {disruptiva['EMPRESA']}"
    )