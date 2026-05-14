import streamlit as st
import plotly.express as px

def render_clustering(df):

    st.subheader("🌐 Corporate Strategic Map")

    # =====================================================
    # FILTROS
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:

        clusters = st.multiselect(
            "🎯 Filtrar clusters",
            sorted(df["CLUSTER"].unique()),
            default=sorted(df["CLUSTER"].unique())
        )

    with c2:

        score_min = st.slider(
            "📈 Score mínimo",
            0.0,
            7.0,
            3.0,
            0.1
        )

    # =====================================================
    # FILTRADO
    # =====================================================

    mapa_df = df[
        (df["CLUSTER"].isin(clusters)) &
        (df["SCORE_TOTAL"] >= score_min)
    ]

    # =====================================================
    # TOP EMPRESAS
    # =====================================================

    mapa_df = mapa_df.sort_values(
        by="SCORE_TOTAL",
        ascending=False
    ).head(25)

    # =====================================================
    # SCATTER PREMIUM
    # =====================================================

    fig = px.scatter(
        mapa_df,
        x="X",
        y="Y",
        color="CLUSTER",
        size="SCORE_TOTAL",
        text="EMPRESA",
        hover_name="EMPRESA",
        hover_data={
            "SCORE_TOTAL": True,
            "ESG_SCORE": True,
            "CLASIFICACION": True,
            "CLUSTER": True,
            "X": False,
            "Y": False
        },
        size_max=55,
        height=750,
        color_continuous_scale="Turbo"
    )

    # =====================================================
    # ESTILO PREMIUM
    # =====================================================

    fig.update_traces(

        textposition="top center",

        marker=dict(
            opacity=0.82,
            line=dict(
                width=2,
                color="white"
            )
        ),

        textfont=dict(
            size=10
        ),

        hovertemplate="""
        <b>%{hovertext}</b><br><br>

        📈 Score Estratégico:
        %{customdata[0]}<br>

        🌱 ESG Score:
        %{customdata[1]}<br>

        🏅 Clasificación:
        %{customdata[2]}<br>

        🧠 Cluster:
        %{customdata[3]}

        <extra></extra>
        """
    )

    # =====================================================
    # LAYOUT
    # =====================================================

    fig.update_layout(

        template="plotly_white",

        title={
            "text": "🌍 Mapa Estratégico Inteligente",
            "x": 0.5
        },

        title_font_size=30,

        paper_bgcolor="#f4f7fb",

        plot_bgcolor="white",

        font=dict(
            family="Arial",
            size=13
        ),

        xaxis=dict(
            showgrid=True,
            gridcolor="#e5e7eb",
            zeroline=False
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="#e5e7eb",
            zeroline=False
        )
    )

    # =====================================================
    # RENDER
    # =====================================================

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # TABLA
    # =====================================================

    st.subheader("📊 Empresas destacadas")

    st.dataframe(
        mapa_df[
            [
                "EMPRESA",
                "SCORE_TOTAL",
                "ESG_SCORE",
                "CLASIFICACION",
                "CLUSTER"
            ]
        ],
        use_container_width=True,
        height=450
    )