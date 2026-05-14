import streamlit as st
import unicodedata


def render_chatbot(df):

    # =====================================================
    # LIMPIAR TEXTO
    # =====================================================

    def limpiar_texto(texto):

        texto = texto.lower()

        texto = unicodedata.normalize(
            'NFD',
            texto
        ).encode(
            'ascii',
            'ignore'
        ).decode("utf-8")

        return texto

    # =====================================================
    # UI
    # =====================================================

    st.subheader("🤖 IA Estratégica Empresarial")

    pregunta = st.text_input(
        "Pregunta algo sobre empresas, sectores o inversión..."
    )

    respuesta = ""

    # =====================================================
    # PROCESAMIENTO
    # =====================================================

    if pregunta:

        q = limpiar_texto(pregunta)

        # =====================================================
        # MEJOR EMPRESA GENERAL
        # =====================================================

        if (
            "mejor empresa" in q or
            "mejor puntuacion global" in q or
            "mejor score" in q
        ):

            top = df.sort_values(
                by="SCORE_TOTAL",
                ascending=False
            ).iloc[0]

            respuesta = f"""
🏆 La mejor empresa actualmente es:

✅ {top['EMPRESA']}

📈 Score Global: {round(top['SCORE_TOTAL'],2)}

🌱 ESG: {round(top['ESG_SCORE'],2)}

🏅 Clasificación: {top['CLASIFICACION']}
"""

        # =====================================================
        # PEOR EMPRESA
        # =====================================================

        elif (
            "no debo invertir" in q or
            "peor empresa" in q or
            "mayor riesgo" in q
        ):

            worst = df.sort_values(
                by="SCORE_TOTAL",
                ascending=True
            ).iloc[0]

            respuesta = f"""
⚠️ Empresa con mayor riesgo estratégico:

❌ {worst['EMPRESA']}

📉 Score: {round(worst['SCORE_TOTAL'],2)}

🏅 Clasificación: {worst['CLASIFICACION']}
"""

        # =====================================================
        # ESG / SOSTENIBILIDAD
        # =====================================================

        elif (
            "mejor esg" in q or
            "sostenibilidad" in q or
            "mejor sostenibilidad" in q
        ):

            top = df.sort_values(
                by="ESG_SCORE",
                ascending=False
            ).iloc[0]

            respuesta = f"""
🌱 Empresa con mejor desempeño ESG:

✅ {top['EMPRESA']}

🌱 ESG Score: {round(top['ESG_SCORE'],2)}

📈 Sostenibilidad: {top['SOSTENIBILIDAD']}
"""

        # =====================================================
        # FINANZAS
        # =====================================================

        elif (
            "financiera" in q or
            "finanzas" in q or
            "puntuacion financiera" in q
        ):

            top = df.sort_values(
                by="FINANZAS",
                ascending=False
            ).iloc[0]

            respuesta = f"""
💰 Empresa con mejor puntuación financiera:

🏆 {top['EMPRESA']}

📈 Finanzas: {top['FINANZAS']}
"""

        # =====================================================
        # COMERCIAL
        # =====================================================

        elif (
            "comercial" in q or
            "ventas" in q
        ):

            top = df.sort_values(
                by="COMERCIAL",
                ascending=False
            ).iloc[0]

            respuesta = f"""
📊 Empresa líder en área comercial:

🏆 {top['EMPRESA']}

📈 Comercial: {top['COMERCIAL']}
"""

        # =====================================================
        # OPERACIONES
        # =====================================================

        elif "operaciones" in q:

            top = df.sort_values(
                by="OPERACIONES",
                ascending=False
            ).iloc[0]

            respuesta = f"""
🏭 Empresa líder en operaciones:

🏆 {top['EMPRESA']}

📈 Operaciones: {top['OPERACIONES']}
"""

        # =====================================================
        # FORMACION
        # =====================================================

        elif (
            "formacion" in q or
            "talento" in q or
            "capital humano" in q
        ):

            top = df.sort_values(
                by="FORMACION",
                ascending=False
            ).iloc[0]

            respuesta = f"""
🎓 Empresa líder en formación:

🏆 {top['EMPRESA']}

📈 Formación: {top['FORMACION']}
"""

        # =====================================================
        # EMPRESAS A
        # =====================================================

        elif (
            "clasificacion a" in q or
            "empresas clasificacion a" in q or
            "empresas son clasificacion a" in q or
            "empresas a" in q
        ):

            ranking = df[
                df["CLASIFICACION"] == "A"
            ]

            if len(ranking) > 0:

                texto = "\n".join(
                    [f"✅ {n}" for n in ranking["EMPRESA"]]
                )

                respuesta = f"""
🏆 Empresas clasificación A:

{texto}
"""

            else:

                respuesta = """
⚠️ No existen empresas clasificación A actualmente.
"""

        # =====================================================
        # EMPRESAS B
        # =====================================================

        elif (
            "clasificacion b" in q or
            "empresas b" in q
        ):

            ranking = df[
                df["CLASIFICACION"] == "B"
            ]

            texto = "\n".join(
                [f"🟡 {n}" for n in ranking["EMPRESA"]]
            )

            respuesta = f"""
📊 Empresas clasificación B:

{texto}
"""

        # =====================================================
        # EMPRESAS C
        # =====================================================

        elif (
            "clasificacion c" in q or
            "empresas c" in q
        ):

            ranking = df[
                df["CLASIFICACION"] == "C"
            ]

            texto = "\n".join(
                [f"🔴 {n}" for n in ranking["EMPRESA"]]
            )

            respuesta = f"""
⚠️ Empresas clasificación C:

{texto}
"""

        # =====================================================
        # RANKING
        # =====================================================

        elif (
            "ranking" in q or
            "top empresas" in q
        ):

            top5 = df.sort_values(
                by="SCORE_TOTAL",
                ascending=False
            ).head(5)

            texto = ""

            for i, row in enumerate(
                top5.itertuples(),
                start=1
            ):

                texto += f"""
{i}. {row.EMPRESA}
📈 Score: {round(row.SCORE_TOTAL,2)}

"""

            respuesta = f"""
🏆 Ranking Corporativo:

{texto}
"""
        # =====================================================
        # COMPARADOR EMPRESARIAL
        # =====================================================

        elif (
            "vs" in q or
            "comparar" in q or
            "mejor entre" in q
        ):

            empresas = df["EMPRESA"].tolist()

            encontrada = []

            for empresa in empresas:

                nombre = limpiar_texto(
                    empresa
                )

                if nombre in q:

                    encontrada.append(
                        empresa
                    )

            if len(encontrada) >= 2:

                emp1 = df[
                    df["EMPRESA"] == encontrada[0]
                ].iloc[0]

                emp2 = df[
                    df["EMPRESA"] == encontrada[1]
                ].iloc[0]

                score1 = emp1["SCORE_TOTAL"]
                score2 = emp2["SCORE_TOTAL"]

                if score1 > score2:

                    mejor = encontrada[0]

                else:

                    mejor = encontrada[1]

                respuesta = f"""
⚔️ Comparativa estratégica:

🏢 {encontrada[0]}
📈 Score: {round(score1,2)}
🌱 ESG: {round(emp1['ESG_SCORE'],2)}

VS

🏢 {encontrada[1]}
📈 Score: {round(score2,2)}
🌱 ESG: {round(emp2['ESG_SCORE'],2)}

🏆 Empresa más sólida:

✅ {mejor}
"""

            else:

                respuesta = """
⚠️ No pude identificar correctamente dos empresas.

Prueba por ejemplo:

• Compara Indra vs Telefónica
• ¿Qué empresa es mejor entre Repsol e Iberdrola?
"""
        # =====================================================
        # DEFAULT
        # =====================================================

        else:

            respuesta = """
🤖 IA Estratégica:

Todavía estoy aprendiendo esa consulta.

Prueba preguntas como:

• ¿Qué empresa no debo invertir?
• ¿Cuál es la mejor empresa?
• ¿Qué empresa tiene mejor ESG?
• ¿Qué empresa tiene mejor puntuación financiera?
• ¿Qué empresas son clasificación A?
• ¿Cuál es el ranking de empresas?
• ¿Qué empresa tiene mejor sostenibilidad?
"""

        st.success(respuesta)