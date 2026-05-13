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

# =====================================================
# TÍTULO PRINCIPAL
# =====================================================

st.title("📊 CMI con Sostenibilidad y Clustering Estratégico")

st.markdown("""
Sistema inteligente de análisis empresarial basado en:

- Cuadro de Mando Integral (CMI)
- Sostenibilidad
- Clustering estratégico
- Analítica visual interactiva
""")

# =====================================================
# SUBIR EXCEL
# =====================================================

archivo = st.file_uploader(
    "📂 Sube tu Excel (.xlsx)",
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
        # LIMPIEZA DATOS
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
        # KPIs EJECUTIVOS
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
            mejor_empresa
        )

        col4.metric(
            "🧠 Cluster Dominante",
            cluster_dominante
        )

        st.divider()

        # =====================================================
        # BUSCADOR EMPRESA
        # =====================================================

        empresa_seleccionada = st.selectbox(
            "🔍 Buscar empresa",
            df_filtrado["EMPRESA"].unique()
        )

        empresa_info = df_filtrado[
            df_filtrado["EMPRESA"] == empresa_seleccionada
        ]

        st.info(
            f"""
            Empresa seleccionada: {empresa_seleccionada}

            Score total: {round(float(empresa_info['SCORE_TOTAL'].values[0]),2)}

            Clasificación: {empresa_info['CLASIFICACION'].values[0]}

            Cluster: {empresa_info['CLUSTER'].values[0]}
            """
        )

        # =====================================================
        # INSIGHTS AUTOMÁTICOS
        # =====================================================

        st.subheader("🧠 Insights automáticos")

        mejor_area = df_filtrado[
            [
                "FINANZAS",
                "COMERCIAL",
                "OPERACIONES",
                "FORMACION",
                "SOSTENIBILIDAD"
            ]
        ].mean().idxmax()

        peor_area = df_filtrado[
            [
                "FINANZAS",
                "COMERCIAL",
                "OPERACIONES",
                "FORMACION",
                "SOSTENIBILIDAD"
            ]
        ].mean().idxmin()

        st.success(
            f"""
            📌 Área con mejor desempeño: {mejor_area}

            📌 Área más débil: {peor_area}

            📌 El cluster dominante actual es el {cluster_dominante}
            """
        )

        st.divider()

        # =====================================================
        # TABS PRINCIPALES
        # =====================================================

        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Resumen Ejecutivo",
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

            ax.tick_params(
                axis='y',
                labelsize=8
            )

            ax.tick_params(
                axis='x',
                labelsize=10
            )

            st.pyplot(fig)

        # =====================================================
        # TAB 3
        # =====================================================

        with tab3:

            st.subheader("🧠 Mapa estratégico interactivo")

            fig2 = px.scatter(
                df_filtrado,
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
                height=700
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

            st.subheader("📊 Empresas por clúster")

            st.dataframe(
                df_filtrado[
                    [
                        "EMPRESA",
                        "CLUSTER",
                        "SCORE_TOTAL",
                        "CLASIFICACION"
                    ]
                ],
                use_container_width=True,
                height=400
            )

        # =====================================================
        # TAB 4
        # =====================================================

        with tab4:

            st.subheader("📥 Exportar datos")

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