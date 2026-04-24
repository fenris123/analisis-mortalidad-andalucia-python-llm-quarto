# -*- coding: utf-8 -*-
"""
Indicadores SNS Andalucía 2003 vs 2023
Tasa de mortalidad
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import requests
import subprocess



# ==============================
# 1. RUTA BASE (PORTABLE) Y DEFINICIÓN NOMBRE ARCHIVOS
# ==============================

base_dir = Path(__file__).resolve().parent

file_2003 = base_dir / "entrada" / "Perfil_Andalucía_2003.xls"
file_2023 = base_dir / "entrada" / "Perfil_Andalucía_2023.xls"

reporte_dir = base_dir / "reporte"
reporte_dir.mkdir(exist_ok=True)





# ==============================
# 2. FUNCIÓN DE CARGA Y LIMPIEZA
# ==============================

def load_sns_file(file_path, year):

    df = pd.read_excel(
        file_path,
        engine="xlrd",
        header=3
    )

    df = df[df.iloc[:, 0].astype(str).str.startswith("Tasa de mortalidad")].copy()

    cols_base = [
        "Indicador",
        "Valor nacional",
        "Valor de Andalucía (AN)",
        "Máximo",
        "Mínimo",
        "Rango intercuartílico"
    ]

    df = df[cols_base].copy()

    cols_num = cols_base[1:]

    for col in cols_num:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    rename_map = {
        "Valor nacional": f"Valor nacional_{year}",
        "Valor de Andalucía (AN)": f"Valor Andalucía_{year}",
        "Máximo": f"Máximo_{year}",
        "Mínimo": f"Mínimo_{year}",
        "Rango intercuartílico": f"Rango intercuartílico_{year}"
    }

    df = df.rename(columns=rename_map)

    df["Indicador"] = df["Indicador"].astype(str).str.strip()
    df.reset_index(drop=True, inplace=True)

    return df


df_2003 = load_sns_file(file_2003, "2003")
df_2023 = load_sns_file(file_2023, "2023")


df_final = pd.merge(
    df_2003,
    df_2023,
    on="Indicador",
    how="inner"
)



# ==============================
# 3. COLUMNA DESCRIPCIONES
# ==============================

mapeo_descripciones = {
    "Tasa de mortalidad ajustada por edad por cardiopatía isquémica por 100 000 hab.": "TM Cardiopatía",
    "Tasa de mortalidad ajustada por edad, por enfermedad cerebrovascular por 100 000 hab.": "TM Cerebrovascular",
    "Tasa de mortalidad ajustada por edad por cáncer, por 100 000 hab.": "TM Cáncer",
    "Tasa de mortalidad ajustada por edad por enfermedad pulmonar obstructiva crónica, por 100 000 hab.": "TM EPOC",
    "Tasa de mortalidad ajustada por edad por diabetes mellitus, por 100 000 hab.": "TM Diabetes",
    "Tasa de mortalidad ajustada por edad por enfermedad crónica del hígado, por 100 000 hab.": "TM Enf. Hepática crónica",
    "Tasa de mortalidad ajustada por edad por suicidio, por 100 000 hab.": "TM Suicidio",
    "Tasa de mortalidad ajustada por edad por neumonía e influenza, por 100 000 hab.": "TM Neumonía y gripe",
    "Tasa de mortalidad infantil por 1000 nacidos vivos": "TM Infantil",
    "Tasa de mortalidad prematura por cardiopatía isquémica, ajustada por edad, por 100 000 hab.": "TMP Cardiopatía isquémica",
    "Tasa de mortalidad prematura por enfermedad vascular cerebral, ajustada por edad, por 100 000 hab.": "TMP Cerebrovascular",
    "Tasa de mortalidad prematura por cáncer, ajustada por edad, por 100 000 hab": "TMP Cáncer",
    "Tasa de mortalidad prematura por EPOC, ajustada por edad, por 100 000 hab.": "TMP EPOC",
    "Tasa de mortalidad prematura por diabetes mellitus, ajustada por edad, por 100 000 hab.": "TMP Diabetes"
}

df_final["Descripcion"] = df_final["Indicador"].map(mapeo_descripciones)


# ==============================
# 4. COLUMNA VARIACIÓN
# ==============================

df_final["Variacion_Andalucia"] = (
    (df_final["Valor Andalucía_2023"] - df_final["Valor Andalucía_2003"]) /
    df_final["Valor Andalucía_2003"]
) * 100

df_final["Variacion_Espana"] = (
    (df_final["Valor nacional_2023"] - df_final["Valor nacional_2003"]) /
    df_final["Valor nacional_2003"]
) * 100


df_final["Variacion_Andalucia"] = df_final["Variacion_Andalucia"].round(2)
df_final["Variacion_Espana"] = df_final["Variacion_Espana"].round(2)



# ==============================
# 5. FUNCIONES DE GRÁFICAS
# ==============================


def save_fig(fig, name):
    fig.savefig(reporte_dir / name, dpi=300, bbox_inches="tight")



def plot_mortalidad(df, col_2003, col_2023, titulo, ylabel, nombre_archivo):

    x = df["Descripcion"]
    pos = np.arange(len(x))
    width = 0.4

    fig, ax = plt.subplots(figsize=(16, 8))

    for spine in ax.spines.values():
        spine.set_color("gray")

    ax.bar(pos - width/2, df[col_2003], width=width,
           color="steelblue", label="2003")

    ax.bar(pos + width/2, df[col_2023], width=width,
           color="steelblue", alpha=0.6, label="2023")

    ax.set_xticks(pos)
    ax.set_xticklabels(x, rotation=45, ha="right", size=14)

    ax.set_title(titulo, size=20)
    ax.set_xlabel("Tipo de mortalidad", size=16)
    ax.set_ylabel(ylabel, size=16)

    ax.legend(fontsize=16)

    fig.text(
        0.01, 0.01,
        "TM = Tasa de mortalidad | TMP = Tasa de mortalidad prematura",
        fontsize=11,
        color="dimgray"
    )

    plt.tight_layout()

    save_fig(fig, nombre_archivo + ".png")
    plt.show()


def plot_descenso(df, col_andalucia, col_espana, titulo, nombre_archivo):

    x = df["Descripcion"]

    y_and = abs(df[col_andalucia])
    y_esp = abs(df[col_espana])

    pos = np.arange(len(x))
    width = 0.4

    fig, ax = plt.subplots(figsize=(16, 8))

    for spine in ax.spines.values():
        spine.set_color("gray")

    ax.bar(pos - width/2, y_and, width=width,
           color="steelblue", label="Andalucía")

    ax.bar(pos + width/2, y_esp, width=width,
           color="steelblue", alpha=0.6, label="España")

    ax.set_xticks(pos)
    ax.set_xticklabels(x, rotation=45, ha="right", size=14)

    ax.set_title(titulo, size=20)
    ax.set_xlabel("Tipo de mortalidad", size=16)
    ax.set_ylabel("Descenso (%)", size=16)

    ax.legend(fontsize=16)

    plt.tight_layout()

    save_fig(fig, nombre_archivo + ".png")
    plt.show()


def plot_rango(df, col_andalucia, col_espana, col_min, col_max, titulo, nombre_archivo):

    x = df["Descripcion"]
    pos = np.arange(len(x))

    y_and = df[col_andalucia].values
    y_esp = df[col_espana].values
    y_min = df[col_min].values
    y_max = df[col_max].values

    fig, ax = plt.subplots(figsize=(16, 8))

    for spine in ax.spines.values():
        spine.set_color("gray")

    ax.vlines(pos, y_min, y_max, color="dimgray", linewidth=20, alpha=0.6)

    ax.scatter(pos, y_and, color="darkblue", label="Andalucía",
               marker="_", s=800, linewidths=3)

    ax.scatter(pos, y_esp, color="steelblue", label="España",
               marker="_", s=800, linewidths=3)

    ax.set_xticks(pos)
    ax.set_xticklabels(x, rotation=45, ha="right", size=14)

    ax.set_title(titulo, size=20)
    ax.set_xlabel("Tipo de mortalidad", size=16)
    ax.set_ylabel("Tasa de mortalidad", size=16)

    ax.legend(fontsize=16)

    plt.tight_layout()

    save_fig(fig, nombre_archivo + ".png")
    plt.show()




# ==============================
# 6. EJECUCIÓN DE GRAFICAS
# ==============================

plot_mortalidad(
    df_final,
    "Valor Andalucía_2003",
    "Valor Andalucía_2023",
    "Tasa de mortalidad Andalucía 2003 vs 2023",
    "Valor Andalucía",
    "Grafica_mortalidad_AND"
)

plot_mortalidad(
    df_final,
    "Valor nacional_2003",
    "Valor nacional_2023",
    "Tasa de mortalidad España 2003 vs 2023",
    "Valor nacional",
    "Grafica_mortalidad_ESP"
)

plot_descenso(
    df_final,
    "Variacion_Andalucia",
    "Variacion_Espana",
    "Descenso porcentual mortalidad 2003-2023",
    "Grafica_descenso"
)


plot_rango(
    df_final,
    "Valor Andalucía_2023",
    "Valor nacional_2023",
    "Mínimo_2023",
    "Máximo_2023",
    "Posición en rango nacional 2023",
    "Grafica_rango"
)




# ==============================
# 7. ANALISIS LLM (3 SECCIONES)
# ==============================

def analisis_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1:8b",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Eres un analista de datos sanitarios. "
                        "Redacta informes técnicos claros, sin inventar datos. "
                        "Sé conciso y estructurado."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "stream": False
        }
    )

    return response.json()["message"]["content"].strip()


# =============
# SECCIÓN 1
# =============

prompt_mortalidad = f"""
Analiza la evolución de las tasas de mortalidad entre 2003 y 2023.

ANDALUCÍA:
{df_final[['Descripcion', 'Valor Andalucía_2003', 'Valor Andalucía_2023']].to_string(index=False)}

ESPAÑA:
{df_final[['Descripcion', 'Valor nacional_2003', 'Valor nacional_2023']].to_string(index=False)}

Incluye:
- tendencias generales
- diferencias relevantes entre territorios
"""


# =============
# SECCIÓN 2
# =============

prompt_variacion = f"""
Analiza la variación porcentual de mortalidad entre 2003 y 2023.

ANDALUCÍA:
{df_final[['Descripcion', 'Variacion_Andalucia']].to_string(index=False)}

ESPAÑA:
{df_final[['Descripcion', 'Variacion_Espana']].to_string(index=False)}

Explica:
- qué causas mejoran más
- cuáles mejoran menos o empeoran
- diferencias territoriales
"""


# ==========================
# SECCIÓN 3
# ==========================

prompt_rango = f"""
Analiza la posición de Andalucía y España dentro del rango nacional (mínimo-máximo).

DATOS 2023:
{df_final[['Descripcion', 'Valor Andalucía_2023', 'Valor nacional_2023', 'Mínimo_2023', 'Máximo_2023']].to_string(index=False)}

Explica:
- en qué indicadores están más cerca del máximo
- en cuáles están más cerca del mínimo
- interpretación sanitaria global
"""


# ==============================
# 8. EJECUCIÓN LLM
# ==============================

texto_mortalidad = analisis_llm(prompt_mortalidad)
texto_variacion = analisis_llm(prompt_variacion)
texto_rango = analisis_llm(prompt_rango)




# ==============================
# 9. GUARDAR TEXTOS EN /reporte
# ==============================

reporte_dir = base_dir / "reporte"
reporte_dir.mkdir(exist_ok=True)

(reporte_dir / "texto_mortalidad.txt").write_text(
    texto_mortalidad,
    encoding="utf-8"
)

(reporte_dir / "texto_variacion.txt").write_text(
    texto_variacion,
    encoding="utf-8"
)

(reporte_dir / "texto_rango.txt").write_text(
    texto_rango,
    encoding="utf-8"
)




# ==============================
# 10. GENERAR INFORME QUARTO
# ==============================

qmd_path = reporte_dir / "reporte.qmd"

qmd_content = """
---
title: "Análisis mortalidad SNS Andalucía 2003 vs 2023"
format: pdf
---

## 1. Evolución de la mortalidad

""" + (reporte_dir / "texto_mortalidad.txt").read_text(encoding="utf-8") + """

![](Grafica_mortalidad_AND.png)

![](Grafica_mortalidad_ESP.png)

---

## 2. Variación porcentual

""" + (reporte_dir / "texto_variacion.txt").read_text(encoding="utf-8") + """

![](Grafica_descenso.png)

---

## 3. Posición en el rango nacional

""" + (reporte_dir / "texto_rango.txt").read_text(encoding="utf-8") + """

![](Grafica_rango.png)
"""




qmd_path = reporte_dir / "reporte.qmd"
qmd_path = qmd_path.resolve()


if not qmd_path.exists():
    print(f"Error: El archivo {qmd_path} no se ha creado.")
else:
    # Usamos os.path.normpath para asegurar que los separadores sean los correctos para Windows
    # Y cambiamos el directorio de trabajo (cwd) al directorio del reporte
    # Esto ayuda a Quarto a encontrar las imágenes y archivos .txt locales

    try:
        resultado = subprocess.run(
            ["quarto", "render", qmd_path.name, "--to", "pdf"],
            cwd=str(qmd_path.parent), # Ejecutamos DESDE la carpeta del reporte
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        if resultado.returncode != 0:
            print("Error en Quarto:")
            print(resultado.stderr)
        else:
            print("Informe generado con éxito.")

    except FileNotFoundError:
        print("Error: Quarto no está instalado o no se encuentra en el PATH.")
