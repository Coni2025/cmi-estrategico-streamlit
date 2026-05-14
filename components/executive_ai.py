import streamlit as st
import pandas as pd


def render_executive_ai(df):

    st.subheader("🧠 IA Ejecutiva Corporativa")

    # =====================================================
    # RESUMEN GENERAL
    # =====================================================

    promedio = round(
        df["SCORE_TOTAL"].mean(),
        2
    )

    esg = round(
        df["ESG_SCORE"].mean(),
        2
    )

    mejor = df.sort_values(
        by="SCORE_TOTAL",
        ascending=False
    ).iloc[0]

    peor = df.sort_values(
        by="SCORE_TOTAL",
        ascending=True
    ).iloc[0]

    st.markdown("## 📊 Diagnóstico Ejecutivo")

    st.info(f"""
📈 Score promedio corporativo: {promedio}

🌱 ESG promedio: {esg}

🏆 Empresa líder:
{mejor['EMPRESA']}

⚠️ Empresa con mayor riesgo:
{peor['EMPRESA']}
""")

    # =====================================================
    # INSIGHTS IA
    # =====================================================

    st.markdown("## 🤖 Insights Estratégicos IA")

    insights = []

    # ESG BAJO

    if esg < 3:

        insights.append(
            "🌱 El ecosistema corporativo presenta baja madurez ESG."
        )

    else:

        insights.append(
            "🌱 Las empresas muestran buen desempeño sostenible."
        )

    # SCORE BAJO

    if promedio < 3:

        insights.append(
            "⚠️ Existe riesgo corporativo general elevado."
        )

    else:

        insights.append(
            "📈 El mercado presenta estabilidad estratégica."
        )

    # CLUSTERS

    cluster_dom = int(
        df["CLUSTER"].mode()[0]
    )

    insights.append(
        f"🧠 El cluster dominante actual es el grupo {cluster_dom}."
    )

    # EMPRESA TOP

    insights.append(
        f"🏆 {mejor['EMPRESA']} lidera el ecosistema empresarial."
    )

    for ins in insights:

        st.success(ins)

    # =====================================================
    # RECOMENDACIONES
    # =====================================================

    st.markdown("## 💡 Recomendaciones IA")

    recomendaciones = []

    recomendaciones.append(
        "Diversificar inversión entre empresas con alto ESG."
    )

    recomendaciones.append(
        "Priorizar empresas clasificación A y B."
    )

    recomendaciones.append(
        "Evitar compañías con score inferior a 2."
    )

    recomendaciones.append(
        "Monitorear sectores con fuerte crecimiento estratégico."
    )

    for r in recomendaciones:

        st.warning(f"✅ {r}")

    # =====================================================
    # EMPRESAS MÁS SÓLIDAS
    # =====================================================

    st.markdown("## 🏆 Top Empresas Estratégicas")

    top = df.sort_values(
        by="SCORE_TOTAL",
        ascending=False
    ).head(10)

    st.dataframe(
        top[
            [
                "EMPRESA",
                "SCORE_TOTAL",
                "ESG_SCORE",
                "CLASIFICACION"
            ]
        ],
        use_container_width=True
    )

    # =====================================================
    # EMPRESAS RIESGO
    # =====================================================

    st.markdown("## ⚠️ Empresas Bajo Riesgo de Inversión")

    riesgo = df.sort_values(
        by="SCORE_TOTAL",
        ascending=False
    ).head(5)

    st.dataframe(
        riesgo[
            [
                "EMPRESA",
                "SCORE_TOTAL",
                "ESG_SCORE"
            ]
        ],
        use_container_width=True
    )

    # =====================================================
    # CONCEPTOS IA
    # =====================================================

    st.markdown("## 📚 Conceptos Estratégicos")

    with st.expander("🌱 ¿Qué es ESG?"):

        st.write("""
ESG significa:

- Environmental
- Social
- Governance

Evalúa sostenibilidad y riesgo empresarial.
""")

    with st.expander("🧠 ¿Qué es clustering empresarial?"):

        st.write("""
El clustering agrupa empresas similares usando Machine Learning.
""")

    with st.expander("📈 ¿Qué significa Score Estratégico?"):

        st.write("""
Representa el rendimiento global corporativo considerando:
finanzas, operaciones, sostenibilidad y formación.
""")