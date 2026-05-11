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
    page_title="CMI Estratégico",
    layout="wide"
)

st.title("📊 CMI con Sostenibilidad y Clustering Estratégico")

# =====================================================
# SUBIR EXCEL
# =====================================================

archivo = st.file_uploader(
    "Sube tu Excel (.xlsx)",
    type=["xlsx"]
)

# =====================================================
# PROCESAMIENTO
# =====================================================

if archivo:

    df = pd.read_excel(archivo)

    # Normalizar nombres columnas
    df.columns = [c.strip().upper() for c in df.columns]

    # Columnas necesarias
    columnas = [
        "EMPRESA",
        "FINANZAS",
        "COMERCIAL",
        "OPERACIONES",
        "FORMACION",
        "SOSTENIBILIDAD"
    ]

    # Verificar columnas
    faltan = [c for c in columnas if c not in df.columns]

    if faltan:

        st.error(f"Faltan columnas: {faltan}")

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
        # SIDEBAR
        # =====================================================

        st.sidebar.title("⚙️ Configuración")

        area = st.sidebar.selectbox(
            "Selección área estratégica",
            [
                "GLOBAL",
                "FINANZAS",
                "COMERCIAL",
                "OPERACIONES",
                "FORMACION",
                "SOSTENIBILIDAD"
            ]
        )

        # =====================================================
        # FILTRO ÁREA
        # =====================================================

        if area == "GLOBAL":

            df_filtrado = df.copy()

        else:

            df_filtrado = df[df[area] >= 4]

        # =====================================================
        # TABLA PRINCIPAL
        # =====================================================

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
            height=450
        )

        # =====================================================
        # HEATMAP
        # =====================================================

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

        fig, ax = plt.subplots(figsize=(14, altura))

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
            fontsize=20
        )

        ax.tick_params(axis='y', labelsize=8)
        ax.tick_params(axis='x', labelsize=10)

        st.pyplot(fig)

        # =====================================================
        # CLUSTERING
        # =====================================================

        st.subheader("🔵 Clustering de empresas")

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
        # FILTRO MAPA
        # =====================================================

        if area == "GLOBAL":

            mapa_df = df.copy()

        else:

            mapa_df = df[df[area] >= 4]

        # =====================================================
        # MAPA ESTRATÉGICO INTERACTIVO
        # =====================================================

        st.subheader("🧠 Mapa estratégico interactivo")

        fig2 = px.scatter(
            mapa_df,
            x="X",
            y="Y",
            color="CLUSTER",
            size="SCORE_TOTAL",
            hover_name="EMPRESA",
            hover_data={
                "SCORE_TOTAL": True,
                "CLASIFICACION": True,
                "CLUSTER": True,
                "X": False,
                "Y": False
            },
            title=f"Mapa Estratégico - {area}",
            height=850
        )

        fig2.update_traces(
            marker=dict(
                opacity=0.85,
                line=dict(
                    width=1,
                    color="black"
                )
            )
        )

        fig2.update_layout(
            title_font_size=24,
            xaxis_title="Componente Estratégica 1",
            yaxis_title="Componente Estratégica 2",
            template="plotly_white"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # =====================================================
        # TABLA CLUSTERS
        # =====================================================

        st.subheader("📊 Empresas por clúster")

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
            height=500
        )

        # =====================================================
        # EXPORTAR CSV
        # =====================================================

        st.subheader("📥 Exportar datos")

        export_df = mapa_df[
            [
                "EMPRESA",
                "CLUSTER",
                "SCORE_TOTAL",
                "CLASIFICACION"
            ]
        ]

        csv = export_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="empresas_cluster.csv",
            mime="text/csv"
        )