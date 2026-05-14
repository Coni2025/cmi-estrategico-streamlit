import streamlit as st
import unicodedata


def render_chatbot(df):

    # =====================================================
    # LIMPIAR TEXTO
    # =====================================================

    def limpiar_texto(texto):

        texto = str(texto).lower()

        texto = unicodedata.normalize(
            'NFD',
            texto
        ).encode(
            'ascii',
            'ignore'
        ).decode("utf-8")

        texto = (
            texto
            .replace(",", " ")
            .replace(".", " ")
            .replace("-", " ")
            .replace("_", " ")
            .replace("/", " ")
            .replace("(", " ")
            .replace(")", " ")
        )

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
        # MENOR RIESGO
        # =====================================================

        if (
            "menos riesgo" in q or
            "empresa mas segura" in q or
            "empresa segura" in q or
            "bajo riesgo" in q
        ):

            top = df.sort_values(
                by="SCORE_TOTAL",
                ascending=False
            ).iloc[0]

            respuesta = f"""
🛡️ Empresa con menor riesgo estratégico:

🏆 {top['EMPRESA']}

📈 Score Total: {round(top['SCORE_TOTAL'],2)}

🌱 ESG: {round(top['ESG_SCORE'],2)}

🏅 Clasificación: {top['CLASIFICACION']}

✅ Presenta alta estabilidad corporativa.
"""

        # =====================================================
        # MEJOR EMPRESA
        # =====================================================

        elif (
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
        # CLASIFICACION A
        # =====================================================

        elif (
            "clasificacion a" in q or
            "empresas clasificacion a" in q or
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
        # CLASIFICACION B
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
        # CLASIFICACION C
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
        # RANKING TOP
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
        # MEJOR SECTOR
        # =====================================================

        elif (
            "mejor sector" in q or
            "sector lider" in q or
            "sector mas rentable" in q
        ):

            sector_avg = df.groupby(
                "SECTOR"
            )["SCORE_TOTAL"].mean()

            mejor_sector = sector_avg.idxmax()

            valor = round(
                sector_avg.max(),
                2
            )

            respuesta = f"""
🏆 Sector líder actualmente:

📊 {mejor_sector}

📈 Score promedio: {valor}

✅ Presenta el ecosistema corporativo más sólido.
"""

        # =====================================================
        # SECTOR MENOR RIESGO
        # =====================================================

        elif (
            "sector menos riesgo" in q or
            "sector mas seguro" in q or
            "sector menor riesgo" in q
        ):

            sector_avg = df.groupby(
                "SECTOR"
            )["ESG_SCORE"].mean()

            mejor_sector = sector_avg.idxmax()

            valor = round(
                sector_avg.max(),
                2
            )

            respuesta = f"""
🛡️ Sector con menor riesgo estratégico:

🏭 {mejor_sector}

🌱 ESG promedio: {valor}

✅ Alta estabilidad corporativa y sostenibilidad.
"""

        # =====================================================
        # EMPRESAS POR SECTOR
        # =====================================================

        elif (
            "empresas del sector" in q or
            "empresas de sector" in q or
            "sector energia" in q or
            "sector financiero" in q or
            "sector inmobiliario" in q
        ):

            sectores = df["SECTOR"].dropna().unique()

            encontrado = None

            for s in sectores:

                nombre_sector = limpiar_texto(s)

                if nombre_sector in q:

                    encontrado = s
                    break

            if encontrado:

                empresas_sector = df[
                    df["SECTOR"] == encontrado
                ]["EMPRESA"].tolist()

                texto = "\n".join(
                    [f"• {e}" for e in empresas_sector[:20]]
                )

                respuesta = f"""
🏭 Empresas del sector:

📊 {encontrado}

{texto}
"""

            else:

                respuesta = """
⚠️ No pude identificar el sector.

Prueba:

• empresas del sector energia
• empresas del sector inmobiliario
• empresas del sector farmaceutico
"""

        # =====================================================
        # COMPARADOR IA
        # =====================================================

        elif (
            "vs" in q or
            "comparar" in q or
            "mejor entre" in q
        ):

            encontradas = []

            for empresa in df["EMPRESA"]:

                nombre = limpiar_texto(
                    empresa
                )

                palabras = nombre.split()

                coincidencias = 0

                for palabra in palabras:

                    if (
                        len(palabra) > 3 and
                        palabra in q
                    ):

                        coincidencias += 1

                if coincidencias >= 1:

                    encontradas.append(
                        empresa
                    )

            encontradas = list(
                dict.fromkeys(encontradas)
            )

            if len(encontradas) >= 2:

                emp1 = df[
                    df["EMPRESA"] == encontradas[0]
                ].iloc[0]

                emp2 = df[
                    df["EMPRESA"] == encontradas[1]
                ].iloc[0]

                score1 = float(emp1["SCORE_TOTAL"])
                score2 = float(emp2["SCORE_TOTAL"])

                if score1 == 0 and score2 == 0:

                    respuesta = f"""
⚠️ No existen suficientes métricas para comparar:

• {encontradas[0]}
• {encontradas[1]}

La información estratégica todavía es insuficiente.
"""

                else:

                    if score1 > score2:

                        mejor = encontradas[0]

                    else:

                        mejor = encontradas[1]

                    respuesta = f"""
⚔️ Comparación estratégica IA

🏢 {encontradas[0]}
📈 Puntuación: {round(score1,2)}
🌱 ESG: {round(emp1['ESG_SCORE'],2)}

VS

🏢 {encontradas[1]}
📈 Puntuación: {round(score2,2)}
🌱 ESG: {round(emp2['ESG_SCORE'],2)}

🏆 Empresa más sólida:
✅ {mejor}
"""

            else:

                respuesta = """
⚠️ No pude identificar correctamente dos empresas.

Prueba por ejemplo:

• Compara Indra vs Telefónica
• Compara Repsol vs Iberdrola
• Compara Santander vs BBVA
"""

        # =====================================================
        # CONCEPTOS ESG
        # =====================================================

        elif (
            "que es esg" in q or
            "explica esg" in q
        ):

            respuesta = """
🌱 ESG significa:

E → Environmental
S → Social
G → Governance

Es un indicador que evalúa:

• sostenibilidad
• impacto ambiental
• responsabilidad social
• gobernanza empresarial

Las empresas con alto ESG suelen tener:

✅ menor riesgo
✅ mejor reputación
✅ mayor sostenibilidad futura
"""

        # =====================================================
        # CONCEPTOS CLUSTERING
        # =====================================================

        elif (
            "que es clustering" in q or
            "que es cluster" in q
        ):

            respuesta = """
🧠 Clustering empresarial:

Es una técnica de Inteligencia Artificial que agrupa empresas similares según patrones estratégicos.

Por ejemplo:

• empresas financieras
• empresas sostenibles
• empresas de alto crecimiento

La IA detecta automáticamente similitudes usando Machine Learning.
"""

        # =====================================================
        # CONCEPTOS SCORE
        # =====================================================

        elif (
            "que es score" in q or
            "que es score estrategico" in q
        ):

            respuesta = """
📈 Score Estratégico:

Es una puntuación global creada mediante IA analítica.

Evalúa:

• finanzas
• operaciones
• sostenibilidad
• comercial
• formación

Un score alto suele indicar:

✅ mejor estabilidad
✅ mayor capacidad competitiva
✅ menor riesgo empresarial
"""

        # =====================================================
        # DEFAULT
        # =====================================================

        else:

            respuesta = """
🤖 IA Estratégica:

Todavía estoy aprendiendo esa consulta.

Prueba preguntas como:

• ¿Cuál es el mejor sector?
• ¿Qué sector tiene menos riesgo?
• Empresas del sector energía
• ¿Qué empresa no debo invertir?
• ¿Cuál es la mejor empresa?
• ¿Qué empresa tiene mejor ESG?
• ¿Cuál es el ranking de empresas?
• Compara Indra vs Telefónica
• ¿Qué es ESG?
• ¿Qué es clustering?
"""

        st.success(respuesta)