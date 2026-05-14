import random

# =====================================================
# AI SCORING ENGINE
# =====================================================

def generar_metricas_automaticas(df):

    perfiles = {

        "Servicios Financieros": {
            "FINANZAS": 8,
            "COMERCIAL": 7,
            "OPERACIONES": 6,
            "FORMACION": 6,
            "SOSTENIBILIDAD": 5
        },

        "Banca": {
            "FINANZAS": 8,
            "COMERCIAL": 7,
            "OPERACIONES": 6,
            "FORMACION": 6,
            "SOSTENIBILIDAD": 5
        },

        "Energía": {
            "FINANZAS": 7,
            "COMERCIAL": 6,
            "OPERACIONES": 8,
            "FORMACION": 6,
            "SOSTENIBILIDAD": 7
        },

        "Tecnología": {
            "FINANZAS": 7,
            "COMERCIAL": 8,
            "OPERACIONES": 7,
            "FORMACION": 8,
            "SOSTENIBILIDAD": 6
        },

        "Construcción": {
            "FINANZAS": 6,
            "COMERCIAL": 6,
            "OPERACIONES": 8,
            "FORMACION": 5,
            "SOSTENIBILIDAD": 5
        }

    }

    metricas = [
        "FINANZAS",
        "COMERCIAL",
        "OPERACIONES",
        "FORMACION",
        "SOSTENIBILIDAD"
    ]

    for i, row in df.iterrows():

        sector = str(row["SECTOR"]).strip()

        # =====================================================
        # SI EL SECTOR EXISTE
        # =====================================================

        if sector in perfiles:

            perfil = perfiles[sector]

            for m in metricas:

                if row[m] == 0:

                    variacion = random.uniform(-1, 1)

                    valor = perfil[m] + variacion

                    valor = max(3, min(10, valor))

                    df.at[i, m] = round(valor, 1)

        # =====================================================
        # SI EL SECTOR NO EXISTE
        # =====================================================

        else:

            for m in metricas:

                if row[m] == 0:

                    valor = random.uniform(4, 8)

                    df.at[i, m] = round(valor, 1)

    return df