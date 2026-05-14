import streamlit as st


def render_kpis(df):

    promedio = round(
        df["SCORE_TOTAL"].mean(),
        2
    )

    total = len(df)

    esg = round(
        df["ESG_SCORE"].mean(),
        2
    )

    cluster = int(
        df["CLUSTER"].mode()[0]
    )

    c1, c2, c3, c4 = st.columns(4)

    # =====================================================
    # KPI 1
    # =====================================================

    with c1:

        st.markdown(f"""
        <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        box-shadow:0px 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        ">
            <h3>📈 Score Promedio</h3>
            <h1 style='color:#2563eb'>
                {promedio}
            </h1>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # KPI 2
    # =====================================================

    with c2:

        st.markdown(f"""
        <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        box-shadow:0px 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        ">
            <h3>🏢 Empresas</h3>
            <h1 style='color:#16a34a'>
                {total}
            </h1>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # KPI 3
    # =====================================================

    with c3:

        st.markdown(f"""
        <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        box-shadow:0px 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        ">
            <h3>🌱 ESG Score</h3>
            <h1 style='color:#dc2626'>
                {esg}
            </h1>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # KPI 4
    # =====================================================

    with c4:

        st.markdown(f"""
        <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        box-shadow:0px 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        ">
            <h3>🧠 Cluster</h3>
            <h1 style='color:#7c3aed'>
                {cluster}
            </h1>
        </div>
        """, unsafe_allow_html=True)