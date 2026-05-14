import plotly.express as px
import plotly.graph_objects as go
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
from components.executive_ai import render_executive_ai
from components.dashboard import render_dashboard
from components.heatmap import render_heatmap
from components.kpis import render_kpis
from components.ai_scoring import generar_metricas_automaticas
from components.strategic_map import render_strategic_map

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

/* =====================================================
BACKGROUND
===================================================== */

.main {
    background-color: #f4f7fb;
}

/* =====================================================
TITULOS
===================================================== */

h1, h2, h3 {
    color: #111827;
    font-weight: 700;
}

/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #111827 0%,
        #1f2937 100%
    );

    border-right: 1px solid #374151;
}

/* textos sidebar */

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* selectbox */

section[data-testid="stSidebar"] .stSelectbox {

    background-color: #374151;
    border-radius: 12px;
    padding: 5px;
}

/* expanders */

.streamlit-expanderHeader {

    background-color: #1f2937 !important;

    border-radius: 10px;

    padding: 8px;

    font-weight: 600;
}

/* =====================================================
KPI CARDS
===================================================== */

[data-testid="metric-container"]{

    background:white;

    border-radius:18px;

    padding:18px;

    border:1px solid #e5e7eb;

    box-shadow:0px 4px 12px rgba(0,0,0,0.06);
}

/* =====================================================
TABS
===================================================== */

button[data-baseweb="tab"] {

    font-size:16px;

    font-weight:600;
}

/* =====================================================
DATAFRAME
===================================================== */

[data-testid="stDataFrame"] {

    border-radius: 15px;

    overflow:hidden;

    border:1px solid #e5e7eb;
}

/* =====================================================
SUCCESS BOX
===================================================== */

.stAlert {

    border-radius:15px;
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
    # LIMPIEZA NUMERICA
    # =====================================================

    columnas_metricas = [
    "FINANZAS",
    "COMERCIAL",
    "OPERACIONES",
    "FORMACION",
    "SOSTENIBILIDAD"
]

    for col in columnas_metricas:

     df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", ".")
    )

     df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

     df[col] = df[col].fillna(0)

    # =====================================================
    # LIMPIEZA COLUMNAS
    # =====================================================

    df.columns = [c.strip().upper() for c in df.columns]

    columnas = [
        "EMPRESA",
        "SECTOR",
        "FINANZAS",
        "COMERCIAL",
        "OPERACIONES",
        "FORMACION",
        "SOSTENIBILIDAD"
    ]

    # =====================================================
    # LIMPIEZA DATOS
    # =====================================================

    for col in columnas[2:]:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.fillna(0)
    # =====================================================
    # IA SCORING ENGINE
    # =====================================================

    df = generar_metricas_automaticas(df)

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
        [
            "FINANZAS",
            "COMERCIAL",
            "OPERACIONES",
            "FORMACION",
            "SOSTENIBILIDAD"
        ]
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

        render_kpis(df_filtrado)

        # =====================================================
        # CHATBOT
        # =====================================================

        render_chatbot(df_filtrado)

        st.divider()

        # =====================================================
        # TABS
        # =====================================================

        tab1, tab2, tab3, tab4, tab5 , tab6 , tab7 = st.tabs([
            "📊 Dashboard",
            "🌡️ Heatmap",
            "🌐 Clustering",
            "🕸️ Radar",
            "💰 Investment AI",
            "🧠 Executive AI",
            "🗺️ Strategic Map"
        ])

        # =====================================================
        # TAB 1
        # =====================================================

    with tab1:

        render_dashboard(df_filtrado)

        # =====================================================
        # TAB 2
        # =====================================================

    with tab2:
        render_heatmap(df_filtrado)

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
        # =====================================================
        # TAB 6
        # =====================================================

    with tab6:

            render_executive_ai(df_filtrado)
    with tab7:

            render_strategic_map(df_filtrado)