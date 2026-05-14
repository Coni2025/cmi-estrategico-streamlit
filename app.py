import streamlit as st
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from components.sidebar import render_sidebar
from components.chatbot import render_chatbot
from components.clustering import render_clustering
from components.radar import render_radar
from components.investment_ai import render_investment_ai

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="CMI Strategic AI",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #f4f7fb;
}

h1, h2, h3 {
    color: #111827;
    font-weight: 700;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:18px;
    padding:18px;
    border:1px solid #e5e7eb;
    box-shadow:0px 4px 12px rgba(0,0,0,0.06);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.title("📊 IA Ejecutiva Estratégica CMI")

st.markdown("""
### Plataforma inteligente de análisis corporativo

- Inteligencia Estratégica
- ESG Analytics
- Clústeres Empresariales
- IA Financiera
- Análisis Visual
""")

# =====================================================
# UPLOAD
# =====================================================

archivo = st.file_uploader(
    "📂 Sube tu Excel",
    type=["xlsx"]
)

# =====================================================
# MAIN
# =====================================================

if archivo:

    # =====================================================
    # LECTURA EXCEL
    # =====================================================

    df = pd.read_excel(archivo)

    # =====================================================
    # LIMPIEZA COLUMNAS
    # =====================================================

    df.columns = [c.strip().upper() for c in df.columns]

    columnas = [
        "EMPRESA",
        "FINANZAS",
        "COMERCIAL",
        "OPERACIONES",
        "FORMACION",
        "SOSTENIBILIDAD"
    ]

    # =====================================================
    # LIMPIEZA DATOS
    # =====================================================

    for col in columnas[1:]:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.fillna(0)

    df = df.dropna(subset=["EMPRESA"])

    # =====================================================
    # VALIDACION
    # =====================================================

    faltan = [c for c in columnas if c not in df.columns]

    if faltan:

        st.error(f"❌ Faltan columnas: {faltan}")

    else:

        # =====================================================
        # SCORE TOTAL
        # =====================================================

        df["SCORE_TOTAL"] = df[
            columnas[1:]
        ].mean(axis=1)

        # =====================================================
        # ESG SCORE
        # =====================================================

        df["ESG_SCORE"] = (
            df["SOSTENIBILIDAD"] * 0.6 +
            df["FORMACION"] * 0.4
        )

        # =====================================================
        # CLASIFICACION
        # =====================================================

        def clasificar(x):

            if x >= 6:
                return "A"

            elif x >= 4:
                return "B"

            else:
                return "C"

        df["CLASIFICACION"] = df[
            "SCORE_TOTAL"
        ].apply(clasificar)

        # =====================================================
        # CLUSTERING
        # =====================================================

        X = df[
            [
                "FINANZAS",
                "COMERCIAL",
                "OPERACIONES",
                "FORMACION",
                "SOSTENIBILIDAD"
            ]
        ]

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(
            n_clusters=3,
            random_state=42,
            n_init=10
        )

        df["CLUSTER"] = kmeans.fit_predict(X_scaled)

        # =====================================================
        # PCA
        # =====================================================

        pca = PCA(n_components=2)

        coords = pca.fit_transform(X_scaled)

        df["X"] = coords[:, 0]
        df["Y"] = coords[:, 1]

        # =====================================================
        # SIDEBAR
        # =====================================================

        area = render_sidebar()

        # =====================================================
        # FILTRO
        # =====================================================

        if area == "GLOBAL":

            df_filtrado = df.copy()

        else:

            df_filtrado = df[
                df[area] >= 4
            ]

        # =====================================================
        # KPIs
        # =====================================================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "📈 Score Promedio",
            round(
                df_filtrado["SCORE_TOTAL"].mean(),
                2
            )
        )

        c2.metric(
            "🏢 Empresas",
            len(df_filtrado)
        )

        c3.metric(
            "🌱 ESG Score",
            round(
                df_filtrado["ESG_SCORE"].mean(),
                2
            )
        )

        c4.metric(
            "🧠 Cluster Dominante",
            int(df_filtrado["CLUSTER"].mode()[0])
        )

        st.divider()

        # =====================================================
        # CHATBOT
        # =====================================================

        render_chatbot(df_filtrado)

        st.divider()

        # =====================================================
        # TABS
        # =====================================================

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dashboard",
            "🌡️ Heatmap",
            "🌐 Clustering",
            "🕸️ Radar",
            "💰 Investment AI"
        ])

        # =====================================================
        # TAB 1
        # =====================================================

        with tab1:

            st.subheader("📊 Dashboard Ejecutivo")

            st.dataframe(
                df_filtrado,
                use_container_width=True,
                height=500
            )

        # =====================================================
        # TAB 2
        # =====================================================

        with tab2:

            st.subheader("🌡️ Heatmap Estratégico")

            st.info(
                "Próximamente: Heatmap IA avanzado."
            )

        # =====================================================
        # TAB 3
        # =====================================================

        with tab3:

            render_clustering(df_filtrado)

        # =====================================================
        # TAB 4
        # =====================================================

        with tab4:

            render_radar(df_filtrado)

        # =====================================================
        # TAB 5
        # =====================================================

        with tab5:

            render_investment_ai(df_filtrado)