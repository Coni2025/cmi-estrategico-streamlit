import streamlit as st

def render_investment_ai(df):

    st.subheader("💰 Investment AI Engine")

    perfil = st.selectbox(
        "Selecciona perfil de inversión",
        [
            "Conservador",
            "ESG Sostenible",
            "Tecnológico",
            "Crecimiento",
            "Balanceado"
        ]
    )

    # =====================================================
    # LÓGICA IA
    # =====================================================

    if perfil == "Conservador":

        top = df.sort_values(
            by=["FINANZAS","SCORE_TOTAL"],
            ascending=False
        ).head(5)

        descripcion = """
Empresas con estabilidad financiera y menor riesgo relativo.
"""

    elif perfil == "ESG Sostenible":

        top = df.sort_values(
            by=["ESG_SCORE","SOSTENIBILIDAD"],
            ascending=False
        ).head(5)

        descripcion = """
Empresas con mayor sostenibilidad y perfil ESG favorable.
"""

    elif perfil == "Tecnológico":

        top = df.sort_values(
            by=["FORMACION","OPERACIONES"],
            ascending=False
        ).head(5)

        descripcion = """
Empresas con mayor capacidad tecnológica y operativa.
"""

    elif perfil == "Crecimiento":

        top = df.sort_values(
            by=["COMERCIAL","SCORE_TOTAL"],
            ascending=False
        ).head(5)

        descripcion = """
Empresas con mayor potencial de expansión comercial.
"""

    else:

        top = df.sort_values(
            by="SCORE_TOTAL",
            ascending=False
        ).head(5)

        descripcion = """
Empresas con equilibrio estratégico general.
"""

    # =====================================================
    # PANEL IA
    # =====================================================

    st.markdown(f"""
<div style="
padding:25px;
background:linear-gradient(135deg,#ecfeff,#cffafe);
border-radius:18px;
border:1px solid #67e8f9;
">

### 🤖 Diagnóstico IA

{descripcion}

</div>
""", unsafe_allow_html=True)

    # =====================================================
    # TABLA
    # =====================================================

    st.subheader("🏆 Recomendaciones IA")

    st.dataframe(
        top[
            [
                "EMPRESA",
                "SCORE_TOTAL",
                "ESG_SCORE",
                "CLASIFICACION",
                "CLUSTER"
            ]
        ],
        use_container_width=True,
        height=350
    )

    # =====================================================
    # EMPRESA TOP
    # =====================================================

    mejor = top.iloc[0]

    st.success(f"""
🏢 Empresa destacada:

{mejor['EMPRESA']}

📈 Score Estratégico:
{round(mejor['SCORE_TOTAL'],2)}

🌱 ESG:
{round(mejor['ESG_SCORE'],2)}

🧠 Cluster:
{mejor['CLUSTER']}
""")