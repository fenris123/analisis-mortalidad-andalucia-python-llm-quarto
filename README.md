# analisis-mortalidad-andalucia-python-llm-quarto
Proyecto de análisis de la evolución de la mortalidad en Andalucía (2003–2023) frente a España. Implementa un flujo de datos con Python para extracción, transformación y análisis de datos sanitarios, visualización avanzada, uso de LLM para generación de insights automatizados y Quarto para informes reproducibles en PDF.

## Descripción del proyecto

Este proyecto analiza la evolución de distintas tasas de mortalidad en Andalucía comparándolas con los valores de España entre 2003 y 2023. El objetivo es identificar tendencias, diferencias territoriales y evolución relativa de los principales indicadores de salud.

Se ha diseñado como un flujo completo de ingeniería de datos aplicado al ámbito sanitario, integrando adquisición de datos, limpieza, transformación, análisis estadístico, visualización y generación automática de informes.

La fuente de datos proviene del Sistema Nacional de Salud (SNS), concretamente del conjunto de indicadores de mortalidad disponible en:
https://inclasns.sanidad.gob.es/main.html

## Requisitos

Para ejecutar este proyecto es necesario disponer de:

### Software
- Python 3.10 o superior
- Quarto (para la generación del informe en PDF)
- Ollama instalado localmente con el modelo:
  - llama3.1:8b

Quarto puede descargarse desde:
https://quarto.org/

Ollama puede descargarse desde:
https://ollama.com/

### Librerías de Python
El proyecto utiliza las siguientes librerías principales:

- pandas
- numpy
- matplotlib
- requests
- pathlib (estándar de Python)
- subprocess (estándar de Python)

En caso de instalación manual:

pip install pandas numpy matplotlib requests

## Estructura del proyecto

El proyecto sigue una estructura de carpetas clara para garantizar reproducibilidad:

- /entrada  
  Contiene los archivos originales descargados del SNS en formato Excel.  
  Ejemplo: perfiles de mortalidad por año (2003, 2023).

- /reporte  
  Carpeta de salida donde se generan automáticamente:
  - Gráficas en formato PNG
  - Textos analíticos generados por el LLM
  - Informe final en PDF generado con Quarto

- Principal.py (raíz del proyecto)  
  Archivo Python que ejecuta todo el pipeline:
  - carga y limpieza de datos
  - análisis y transformación
  - generación de visualizaciones
  - llamadas al LLM
  - creación del informe con Quarto

## Ejecución del proyecto

1. Colocar los ficheros Excel del SNS en la carpeta /entrada. (Ajustar los nombres en el script si es necesario)
2. Activar entorno virtual (opcional pero recomendado)
3. Ejecutar el script principal:

python Principal.py



## Flujo de trabajo

### 1. Ingesta de datos
- Lectura de ficheros Excel desde la carpeta /entrada
- Selección de indicadores de mortalidad del SNS
- Homogeneización de estructuras entre años

### 2. Transformación y limpieza
- Normalización de formatos numéricos
- Renombrado de variables por año (2003 y 2023)
- Unificación de datasets
- Cálculo de variaciones porcentuales

### 3. Análisis exploratorio
- Comparación entre Andalucía y España
- Análisis de evolución temporal por causa de muerte
- Evaluación de mejoras o empeoramientos
- Posición relativa dentro del rango nacional

### 4. Visualización de datos
- Comparativas temporales (2003 vs 2023)
- Análisis de descenso porcentual
- Representación del rango mínimo–máximo nacional
- Gráficas orientadas a interpretación sanitaria

### 5. Generación de análisis con LLM
- Uso de modelo LLM local (Llama 3.1 vía Ollama)
- Generación automática de interpretación de resultados
- Estructuración en tres bloques:
  - evolución de la mortalidad
  - variación porcentual
  - análisis de posición en rango nacional

### 6. Generación de informe reproducible
- Uso de Quarto para ensamblar el informe final
- Integración de texto + gráficos
- Exportación automática a PDF
- Pipeline completamente reproducible

## Tecnologías utilizadas

- Python (pandas, numpy, matplotlib, requests, subprocess)
- LLM local (Llama 3.1 vía Ollama API)
- Quarto para generación de informes reproducibles
- Excel como fuente de datos del SNS
- Ingeniería de datos aplicada (ETL + reporting automatizado)

## Resultado

El proyecto genera automáticamente:

- Gráficas comparativas en /reporte
- Análisis textual generado por LLM
- Informe final en PDF reproducible con Quarto

Ejemplo de graficas:

<img width="4770" height="2401" alt="Grafica_mortalidad_AND" src="https://github.com/user-attachments/assets/74db5f85-bc7a-4e78-a86d-0044af83e476" />

Se puede ver el reporte completo en el archivo reporte.pdf de este repositorio


## Objetivo

Demostrar la integración de ingeniería de datos, análisis estadístico, visualización e inteligencia artificial generativa en un flujo automatizado aplicado a datos reales de salud pública, con énfasis en reproducibilidad, trazabilidad y generación de informes, realizando un reporte automatizado de los resultados en PDF.

## Nota importante sobre ejecución

La generación del informe en PDF mediante Quarto puede presentar problemas si el proyecto se ejecuta desde ubicaciones en red o dispositivos externos (como una NAS). En estos casos, el renderizado del archivo `.qmd` a PDF puede fallar debido a dependencias de rutas, permisos o gestión de archivos temporales.

Se recomienda ejecutar el proyecto desde el sistema de archivos local del equipo (disco interno del ordenador) para garantizar la correcta generación del informe final en PDF.

## Aviso sobre el uso de los datos

Los datos utilizados en este proyecto provienen del Sistema Nacional de Salud (SNS) a través del portal de indicadores de salud disponible en:
https://inclasns.sanidad.gob.es/main.html

El uso, redistribución y tratamiento de estos datos está sujeto a los términos y condiciones establecidos por el propio organismo responsable. Se recomienda consultar dichas condiciones antes de reutilizar este proyecto o los datos en entornos distintos al análisis personal o académico.

Términos de uso oficiales:
https://inclasns.sanidad.gob.es/terms
