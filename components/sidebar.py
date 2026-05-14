import streamlit as st

def render_sidebar():

    st.sidebar.title("⚙️ Executive Panel")

    area = st.sidebar.selectbox(
        "Área estratégica",
        [
            "GLOBAL",
            "FINANZAS",
            "COMERCIAL",
            "OPERACIONES",
            "FORMACION",
            "SOSTENIBILIDAD"
        ]
    )

    st.sidebar.markdown("---")

    with st.sidebar.expander("📈 Desempeño estratégico"):

        st.write("""
Capacidad de una empresa para alcanzar objetivos competitivos y financieros.

Ejemplo:
Inditex mantiene liderazgo global gracias a eficiencia logística y expansión internacional.
""")

    with st.sidebar.expander("🌱 Sostenibilidad"):

        st.write("""
Evalúa impacto ambiental, social y gobernanza ESG.

Ejemplo:
Empresas energéticas renovables suelen tener mejor perfil ESG.
""")

    with st.sidebar.expander("🧠 Clustering empresarial"):

        st.write("""
La IA agrupa empresas similares mediante machine learning.

Ejemplo:
Empresas tecnológicas pueden compartir patrones estratégicos similares.
""")

    with st.sidebar.expander("📊 Inteligencia visual"):

        st.write("""
Uso de dashboards interactivos para analizar decisiones corporativas.

Ejemplo:
Los mapas estratégicos permiten detectar líderes y riesgos rápidamente.
""")

    return area