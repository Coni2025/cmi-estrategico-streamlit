import streamlit as st
import plotly.graph_objects as go

def render_radar(df):

    st.subheader("🕸️ Comparador Estratégico Radar")

    # =====================================================
    # SELECTORES
    # =====================================================

    empresas = sorted(df["EMPRESA"].unique())

    c1, c2 = st.columns(2)

    with c1:

        empresa_1 = st.selectbox(
            "🏢 Empresa 1",
            empresas,
            index=0
        )

    with c2:

        empresa_2 = st.selectbox(
            "🏢 Empresa 2",
            empresas,
            index=1
        )

    # =====================================================
    # DATOS
    # =====================================================

    e1 = df[df["EMPRESA"] == empresa_1].iloc[0]
    e2 = df[df["EMPRESA"] == empresa_2].iloc[0]

    categorias = [
        "FINANZAS",
        "COMERCIAL",
        "OPERACIONES",
        "FORMACION",
        "SOSTENIBILIDAD"
    ]

    valores1 = [e1[c] for c in categorias]
    valores2 = [e2[c] for c in categorias]

    # cerrar radar
    valores1 += [valores1[0]]
    valores2 += [valores2[0]]
    categorias += [categorias[0]]

    # =====================================================
    # FIGURA
    # =====================================================

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores1,
        theta=categorias,
        fill='toself',
        name=empresa_1
    ))

    fig.add_trace(go.Scatterpolar(
        r=valores2,
        theta=categorias,
        fill='toself',
        name=empresa_2
    ))

    # =====================================================
    # LAYOUT
    # =====================================================

    fig.update_layout(

        title={
            "text": "📊 Comparación Estratégica Multivariable",
            "x": 0.5
        },

        title_font_size=26,

        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0,7]
            )
        ),

        template="plotly_white",

        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # INSIGHTS IA
    # =====================================================

    st.subheader("🤖 Diagnóstico comparativo")

    score1 = e1["SCORE_TOTAL"]
    score2 = e2["SCORE_TOTAL"]

    if score1 > score2:

        ganadora = empresa_1

    else:

        ganadora = empresa_2

    diferencia = round(abs(score1 - score2),2)

    st.markdown(f"""
<div style="
padding:25px;
background:linear-gradient(135deg,#eff6ff,#dbeafe);
border-radius:18px;
border:1px solid #93c5fd;
">

### 🏆 Empresa con mejor perfil estratégico:
## {ganadora}

📈 Diferencia de score:
### {diferencia}

✅ El análisis radar permite detectar ventajas competitivas
en múltiples dimensiones corporativas.

</div>
""", unsafe_allow_html=True)