import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="CMI Estratégico Premium",
    layout="wide"
)

# =====================================================
# CSS PREMIUM
# =====================================================

st.markdown("""
<style>

/* Fondo principal */
.main {
    background-color: #f4f7fb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #111827);
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Títulos */
h1, h2, h3 {
    color: #111827;
    font-weight: 700;
}

/* KPI Cards */
[data-testid="metric-container"] {
    background: white;
    border-radius: 18px;
    padding: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.06);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 16px;
}

.stTabs [data-baseweb="tab"] {
    background-color: white;
    border-radius: 12px;
    padding: 10px 18px;
    border: 1px solid #e5e7eb;
}

/* Selectbox */
.stSelectbox > div > div {
    border-radius: 12px;
    background-color: white;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

/* Botones */
.stButton button {
    border-radius: 12px;
    background-color: #2563eb;
    color: white;
    border: none;
}

/* Caja IA */
.bot-box {
    background: linear-gradient(135deg, #dbeafe, #eff6ff);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #93c5fd;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER PRINCIPAL
# =====================================================

st.title("📊 CMI Estratégico Inteligente")

st.markdown("""
### Plataforma avanzada de analítica empresarial

Sistema inteligente basado en:

- 📈 Cuadro de Mando Integral (CMI)
- 🌱 Sostenibilidad
- 🧠 Clustering estratégico
- 🤖 Inteligencia analítica empresarial
""")

# =====================================================
# SUBIR ARCHIVO
# =====================================================

archivo = st.file_uploader(
    "📂 Sube tu Excel empresarial",
    type=["xlsx"]
)

# =====================================================
# PROCESAMIENTO
# =====================================================

if archivo:

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

    faltan = [c for c in columnas if c not in df.columns]

    if faltan:

        st.error(f"❌ Faltan columnas: {faltan}")

    else:

        # =====================================================
        # LIMPIEZA
        # =====================================================

        df = df.dropna(subset=columnas[1:])

        # =====================================================
        # SCORE TOTAL
        # =====================================================

        df["SCORE_TOTAL"] = df[columnas[1:]].mean(axis=1)

        # =====================================================
        # CLASIFICACIÓN
        # =====================================================

        def clasificar(x):

            if x >= 6:
                return "A"

            elif x >= 4:
                return "B"

            else:
                return "C"

        df["CLASIFICACION"] = df["SCORE_TOTAL"].apply(clasificar)

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

        st.sidebar.title("⚙️ Panel Ejecutivo")

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

        st.sidebar.markdown("""
### 📌 Objetivo

Evaluar empresas mediante:

- desempeño estratégico
- sostenibilidad
- clustering empresarial
- inteligencia visual
""")

        # =====================================================
        # FILTRO
        # =====================================================

        if area == "GLOBAL":

            df_filtrado = df.copy()

        else:

            df_filtrado = df[df[area] >= 4]

        # =====================================================
        # KPIs
        # =====================================================

        promedio_score = round(
            df_filtrado["SCORE_TOTAL"].mean(),
            2
        )

        total_empresas = len(df_filtrado)

        mejor_empresa = df_filtrado.sort_values(
            by="SCORE_TOTAL",
            ascending=False
        ).iloc[0]["EMPRESA"]

        cluster_dominante = (
            df_filtrado["CLUSTER"]
            .mode()[0]
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "📈 Score Promedio",
            promedio_score
        )

        col2.metric(
            "🏢 Empresas",
            total_empresas
        )

        col3.metric(
            "🥇 Mejor Empresa",
            mejor_empresa[:18]
        )

        col4.metric(
            "🧠 Cluster Dominante",
            cluster_dominante
        )

        st.divider()

        # =====================================================
        # BUSCADOR
        # =====================================================

        empresa_seleccionada = st.selectbox(
            "🔎 Buscar empresa",
            df_filtrado["EMPRESA"].unique()
        )

        empresa_info = df_filtrado[
            df_filtrado["EMPRESA"] == empresa_seleccionada
        ]

        st.info(
            f"""
Empresa seleccionada: {empresa_seleccionada}

📈 Score total: {round(float(empresa_info['SCORE_TOTAL'].values[0]),2)}

🏅 Clasificación: {empresa_info['CLASIFICACION'].values[0]}

🧠 Cluster: {empresa_info['CLUSTER'].values[0]}
"""
        )

        # =====================================================
        # IA ESTRATÉGICA
        # =====================================================

        st.subheader("🤖 Asistente Estratégico IA")

        pregunta = st.selectbox(
            "Selecciona una consulta estratégica",
            [
                "¿Cuál es la mejor empresa para invertir?",
                "¿Qué área estratégica tiene mejor desempeño?",
                "¿Cuál es el principal riesgo estratégico?",
                "¿Qué cluster domina actualmente?",
                "¿Qué empresas son más sólidas?"
            ]
        )

        respuesta = ""

        if pregunta == "¿Cuál es la mejor empresa para invertir?":

            top = df_filtrado.sort_values(
                by="SCORE_TOTAL",
                ascending=False
            ).iloc[0]

            respuesta = f"""
La empresa más atractiva actualmente es:

🏢 {top['EMPRESA']}

📈 Score total: {round(top['SCORE_TOTAL'],2)}

🏅 Clasificación: {top['CLASIFICACION']}

Esta empresa presenta el mejor equilibrio estratégico global.
"""

        elif pregunta == "¿Qué área estratégica tiene mejor desempeño?":

            mejor_area = df_filtrado[
                [
                    "FINANZAS",
                    "COMERCIAL",
                    "OPERACIONES",
                    "FORMACION",
                    "SOSTENIBILIDAD"
                ]
            ].mean().idxmax()

            respuesta = f"""
📌 El área con mejor rendimiento promedio es:

✅ {mejor_area}

Esto indica una ventaja competitiva relevante en dicha dimensión.
"""

        elif pregunta == "¿Cuál es el principal riesgo estratégico?":

            peor_area = df_filtrado[
                [
                    "FINANZAS",
                    "COMERCIAL",
                    "OPERACIONES",
                    "FORMACION",
                    "SOSTENIBILIDAD"
                ]
            ].mean().idxmin()

            respuesta = f"""
⚠️ El área más débil actualmente es:

❌ {peor_area}

Se recomienda fortalecer esta dimensión estratégica.
"""

        elif pregunta == "¿Qué cluster domina actualmente?":

            respuesta = f"""
🧠 El cluster dominante actual es:

✅ Cluster {cluster_dominante}

Esto representa el grupo empresarial más frecuente dentro del análisis.
"""

        elif pregunta == "¿Qué empresas son más sólidas?":

            top5 = df_filtrado.sort_values(
                by="SCORE_TOTAL",
                ascending=False
            ).head(5)

            nombres = top5["EMPRESA"].tolist()

            respuesta = "\n".join(
                [f"✅ {n}" for n in nombres]
            )

        st.markdown(
            f"""
<div class="bot-box">
{respuesta}
</div>
""",
            unsafe_allow_html=True
        )

        st.divider()

        # =====================================================
        # TABS
        # =====================================================

        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Dashboard",
            "🔥 Heatmap",
            "🧠 Clustering",
            "📥 Exportación"
        ])

        # =====================================================
        # TAB 1
        # =====================================================

        with tab1:

            st.subheader("📋 Resultados estratégicos")

            st.dataframe(
                df_filtrado[
                    [
                        "EMPRESA",
                        "FINANZAS",
                        "COMERCIAL",
                        "OPERACIONES",
                        "FORMACION",
                        "SOSTENIBILIDAD",
                        "SCORE_TOTAL",
                        "CLASIFICACION"
                    ]
                ],
                use_container_width=True,
                height=500
            )

        # =====================================================
        # TAB 2
        # =====================================================

        with tab2:

            st.subheader("🔥 Heatmap estratégico")

            if area == "GLOBAL":

                heatmap_data = df_filtrado.set_index("EMPRESA")[
                    [
                        "FINANZAS",
                        "COMERCIAL",
                        "OPERACIONES",
                        "FORMACION",
                        "SOSTENIBILIDAD"
                    ]
                ]

            else:

                heatmap_data = df_filtrado.set_index("EMPRESA")[
                    [area]
                ]

            altura = max(8, len(df_filtrado) * 0.35)

            fig, ax = plt.subplots(
                figsize=(14, altura)
            )

            sns.heatmap(
                heatmap_data,
                annot=True,
                cmap="RdYlGn",
                linewidths=0.3,
                linecolor="gray",
                cbar=True,
                annot_kws={"size": 7},
                ax=ax
            )

            ax.set_title(
                f"Heatmap Estratégico - {area}",
                fontsize=18
            )

            st.pyplot(fig)

        # =====================================================
        # TAB 3
        # =====================================================

        with tab3:

             st.subheader("🧠 Mapa Estratégico Inteligente")

    # =====================================================
    # FILTROS AVANZADOS
    # =====================================================

    colf1, colf2 = st.columns(2)

    with colf1:

        cluster_filtro = st.multiselect(
            "🎯 Filtrar clusters",
            options=sorted(df_filtrado["CLUSTER"].unique()),
            default=sorted(df_filtrado["CLUSTER"].unique())
        )

    with colf2:

        score_min = st.slider(
            "📈 Score mínimo",
            0.0,
            7.0,
            3.0,
            0.1
        )

    mapa_df = df_filtrado[
        (df_filtrado["CLUSTER"].isin(cluster_filtro)) &
        (df_filtrado["SCORE_TOTAL"] >= score_min)
    ]

    # =====================================================
    # TOP EMPRESAS
    # =====================================================

    mapa_df = mapa_df.sort_values(
        by="SCORE_TOTAL",
        ascending=False
    ).head(25)

    # =====================================================
    # MAPA PREMIUM
    # =====================================================

    fig2 = px.scatter(

        mapa_df,

        x="X",
        y="Y",

        size="SCORE_TOTAL",

        color="SCORE_TOTAL",

        text=None,

        hover_name="EMPRESA",

        hover_data={

            "SCORE_TOTAL": True,
            "CLASIFICACION": True,
            "CLUSTER": True,

            "FINANZAS": True,
            "COMERCIAL": True,
            "OPERACIONES": True,
            "FORMACION": True,
            "SOSTENIBILIDAD": True,

            "X": False,
            "Y": False
        },

        color_continuous_scale="Turbo",

        height=850,

        title="Mapa Estratégico Corporativo Premium"
    )

    # =====================================================
    # ESTILO EJECUTIVO
    # =====================================================

    fig2.update_traces(

        marker=dict(

            opacity=0.92,

            line=dict(
                width=2,
                color="white"
            )
        )
    )

    fig2.update_layout(

        template="plotly_white",

        title_font_size=30,

        title_x=0.03,

        paper_bgcolor="#f4f7fb",

        plot_bgcolor="#ffffff",

        font=dict(
            family="Arial",
            size=14
        ),

        xaxis=dict(
            title="Componente Estratégica X",
            showgrid=True,
            gridcolor="#e5e7eb"
        ),

        yaxis=dict(
            title="Componente Estratégica Y",
            showgrid=True,
            gridcolor="#e5e7eb"
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # PANEL IA EMPRESA
    # =====================================================

    st.subheader("🤖 Diagnóstico Inteligente Empresarial")

    empresa_ia = st.selectbox(
        "Selecciona empresa para análisis IA",
        mapa_df["EMPRESA"]
    )

    empresa_data = mapa_df[
        mapa_df["EMPRESA"] == empresa_ia
    ].iloc[0]

    # =====================================================
    # ANÁLISIS IA
    # =====================================================

    score = empresa_data["SCORE_TOTAL"]

    finanzas = empresa_data["FINANZAS"]
    comercial = empresa_data["COMERCIAL"]
    operaciones = empresa_data["OPERACIONES"]
    formacion = empresa_data["FORMACION"]
    sostenibilidad = empresa_data["SOSTENIBILIDAD"]

    areas = [
        "FINANZAS",
        "COMERCIAL",
        "OPERACIONES",
        "FORMACION",
        "SOSTENIBILIDAD"
    ]

    mejor_area = empresa_data[areas].idxmax()

    peor_area = empresa_data[areas].idxmin()

    analisis = f"""
### 🏢 Empresa: {empresa_ia}

📈 Score estratégico: {round(score,2)}

🏅 Clasificación: {empresa_data['CLASIFICACION']}

🧠 Cluster: {empresa_data['CLUSTER']}

---

## 📊 Evaluación IA

"""

    if score >= 5:

        analisis += """
✅ Empresa altamente competitiva.

✅ Buen posicionamiento estratégico.

✅ Perfil corporativo sólido para inversión.
"""

    elif score >= 4:

        analisis += """
⚠️ Empresa estable con oportunidades de mejora.

⚠️ Rendimiento estratégico medio.

⚠️ Requiere optimización en ciertas áreas.
"""

    else:

        analisis += """
❌ Empresa vulnerable estratégicamente.

❌ Bajo desempeño global.

❌ Riesgo competitivo elevado.
"""

    analisis += f"""

---

🏆 Área más fuerte:
{mejor_area}

⚠️ Área más débil:
{peor_area}

"""

    if sostenibilidad >= 5:

        analisis += """

🌱 Presenta buen perfil ESG y sostenibilidad empresarial.
"""

    if finanzas >= 5:

        analisis += """

💰 Fortaleza financiera relevante.
"""

    st.markdown(
        f"""
<div class="bot-box">
{analisis}
</div>
""",
        unsafe_allow_html=True
    )

    # =====================================================
    # TABLA CLUSTERS
    # =====================================================

    st.subheader("📊 Empresas destacadas")

    st.dataframe(

        mapa_df[
            [
                "EMPRESA",
                "CLUSTER",
                "SCORE_TOTAL",
                "CLASIFICACION"
            ]
        ],

        use_container_width=True,
        height=450
    )

        # =====================================================
        # TAB 4
        # =====================================================

        with tab4:

            st.subheader("📥 Exportar análisis")

            export_df = df_filtrado[
                [
                    "EMPRESA",
                    "CLUSTER",
                    "SCORE_TOTAL",
                    "CLASIFICACION"
                ]
            ]

            csv = export_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv,
                file_name="empresas_cluster.csv",
                mime="text/csv"
            )

            st.dataframe(
                export_df,
                use_container_width=True
            )