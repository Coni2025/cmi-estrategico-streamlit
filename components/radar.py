import streamlit as st
import plotly.graph_objects as go


def render_radar(df):

    st.subheader("🕸️ Radar Estratégico Empresarial")

    # =====================================================
    # SELECTORES
    # =====================================================

    empresas = sorted(
        df["EMPRESA"].unique()
    )

    col1, col2 = st.columns(2)

    with col1:

        empresa1 = st.selectbox(
            "Empresa 1",
            empresas,
            key="empresa_1"
        )

    with col2:

        empresa2 = st.selectbox(
            "Empresa 2",
            empresas,
            index=1,
            key="empresa_2"
        )

    # =====================================================
    # EXTRAER DATOS
    # =====================================================

    emp1 = df[
        df["EMPRESA"] == empresa1
    ].iloc[0]

    emp2 = df[
        df["EMPRESA"] == empresa2
    ].iloc[0]

    categorias = [
        "FINANZAS",
        "COMERCIAL",
        "OPERACIONES",
        "FORMACION",
        "SOSTENIBILIDAD"
    ]

    valores1 = [
        float(emp1[c])
        for c in categorias
    ]

    valores2 = [
        float(emp2[c])
        for c in categorias
    ]

    # =====================================================
    # VALIDACION
    # =====================================================

    if sum(valores1) == 0:

        st.error(
            f"⚠️ {empresa1} no tiene métricas suficientes."
        )

        return

    if sum(valores2) == 0:

        st.error(
            f"⚠️ {empresa2} no tiene métricas suficientes."
        )

        return

    # =====================================================
    # CERRAR POLIGONO
    # =====================================================

    categorias += [categorias[0]]

    valores1 += [valores1[0]]
    valores2 += [valores2[0]]

    # =====================================================
    # FIGURA
    # =====================================================

    fig = go.Figure()

    # =====================================================
    # EMPRESA 1
    # =====================================================

    fig.add_trace(

        go.Scatterpolar(

            r=valores1,

            theta=categorias,

            fill='toself',

            name=empresa1,

            line=dict(
                color='#2563eb',
                width=4
            ),

            fillcolor='rgba(37,99,235,0.30)',

            marker=dict(
                color='#2563eb',
                size=8
            )
        )
    )

    # =====================================================
    # EMPRESA 2
    # =====================================================

    fig.add_trace(

        go.Scatterpolar(

            r=valores2,

            theta=categorias,

            fill='toself',

            name=empresa2,

            line=dict(
                color='#dc2626',
                width=4
            ),

            fillcolor='rgba(220,38,38,0.30)',

            marker=dict(
                color='#dc2626',
                size=8
            )
        )
    )

    # =====================================================
    # LAYOUT
    # =====================================================

    fig.update_layout(

        title="Interconexión Estratégica Empresarial",

        polar=dict(

            bgcolor="white",

            radialaxis=dict(
                visible=True,
                range=[0,10]
            )
        ),

        showlegend=True,

        height=700,

        paper_bgcolor="white",

        font=dict(
            size=14
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # ANALISIS IA
    # =====================================================

    st.subheader("🧠 Análisis IA")

    score1 = emp1["SCORE_TOTAL"]
    score2 = emp2["SCORE_TOTAL"]

    if score1 > score2:

        mejor = empresa1

    else:

        mejor = empresa2

    st.success(
        f"🏆 La IA detecta que {mejor} presenta mayor fortaleza estratégica global."
    )

    # =====================================================
    # DIFERENCIAS
    # =====================================================

    for c in categorias[:-1]:

        if emp1[c] > emp2[c]:

            st.info(
                f"🔵 {empresa1} lidera en {c}"
            )

        elif emp2[c] > emp1[c]:

            st.info(
                f"🔴 {empresa2} lidera en {c}"
            )