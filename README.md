# 🏠 Barcelona Stays Analysis

Análisis interactivo de alojamientos turísticos en Barcelona basado en datos reales de Inside Airbnb.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.x-blueviolet?style=flat-square&logo=plotly)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas)

## 📊 Demo

> _Captura o GIF del dashboard aquí_

## 🎯 Objetivo

Explorar el mercado de alojamientos turísticos de Barcelona para extraer insights sobre precios, ocupación y distribución geográfica, practicando análisis exploratorio de datos (EDA) y visualización interactiva.

## 🔍 Insights principales

- **Diagonal Mar** lidera en precio medio general, pero al filtrar por apartamentos enteros, **Dreta de l'Eixample** toma el primer puesto.
- Los **apartamentos enteros** representan el 68% de la oferta y tienen el precio medio más alto.
- **Camp d'en Grassot i Gràcia Nova** es el barrio más ocupado pese a no ser de los más caros.
- Existe una **correlación positiva débil** entre precio y puntuación.
- El precio medio real tras eliminar outliers es de **160€/noche**.

## 🛠️ Tecnologías

| Librería | Uso |
|---|---|
| `pandas` | Carga, limpieza y transformación de datos |
| `plotly` | Gráficos interactivos |
| `streamlit` | Dashboard web |
| `matplotlib / seaborn` | Análisis exploratorio |

## 📁 Estructura del proyecto

```
bcn-stays-analysis/
├── data/
│   └── listings.csv.gz       # Dataset de Inside Airbnb (no incluido en el repo)
├── app.py                    # Dashboard Streamlit
├── styles.css                # Estilos personalizados
├── analisis.ipynb            # Notebook de exploración
├── requirements.txt          # Dependencias
└── README.md
```

## 🚀 Cómo ejecutarlo

**1. Clona el repositorio**
```bash
git clone https://github.com/tu-usuario/bcn-stays-analysis.git
cd bcn-stays-analysis
```

**2. Crea el entorno virtual y actívalo**
```bash
python -m venv venv
source venv/bin/activate.fish   # En fish shell
# source venv/bin/activate      # En bash/zsh
```

**3. Instala las dependencias**
```bash
pip install -r requirements.txt
```

**4. Descarga los datos**

Ve a [insideairbnb.com/barcelona](http://insideairbnb.com/barcelona), descarga `listings.csv.gz` y colócalo en la carpeta `data/`.

**5. Lanza el dashboard**
```bash
streamlit run app.py
```

## 📦 Genera el requirements.txt

```bash
pip freeze > requirements.txt
```

## 📌 Fuente de datos

[Inside Airbnb](http://insideairbnb.com) — datos públicos de alojamientos en Barcelona.

---

_Proyecto desarrollado como parte de un portfolio de ciencia de datos._
