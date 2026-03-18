import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Barcelona Stays",
    page_icon="🏠",
    layout="wide"
)

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1>Barcelona Stays</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Análisis interactivo de alojamientos turísticos en Barcelona</p>', unsafe_allow_html=True)

# --- DATOS ---
df = pd.read_csv('data/listings.csv.gz', compression='gzip')

df['price'] = df['price'].str.replace('$', '', regex=False)
df['price'] = df['price'].str.replace(',', '', regex=False)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df = df.dropna(subset=['price'])
df = df[df['price'] >= 10]
df = df[df['price'] <= 1000]

columnas_utiles = [
    'neighbourhood_cleansed', 'room_type',
    'price', 'minimum_nights', 'number_of_reviews',
    'review_scores_rating', 'availability_365', 'accommodates'
]
df = df[columnas_utiles]

# --- SIDEBAR ---
st.sidebar.markdown("# Filtros")

barrios = ['Todos'] + sorted(df['neighbourhood_cleansed'].unique().tolist())
barrio_seleccionado = st.sidebar.selectbox("Barrio", barrios)

tipos = ['Todos'] + sorted(df['room_type'].unique().tolist())
tipo_seleccionado = st.sidebar.selectbox("Tipo de alojamiento", tipos)

precio_min, precio_max = st.sidebar.slider(
    "Rango de precio (€)",
    int(df['price'].min()),
    int(df['price'].max()),
    (10, 500)
)

df_filtrado = df.copy()
if barrio_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['neighbourhood_cleansed'] == barrio_seleccionado]
if tipo_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['room_type'] == tipo_seleccionado]
df_filtrado = df_filtrado[
    (df_filtrado['price'] >= precio_min) &
    (df_filtrado['price'] <= precio_max)
]

# --- MÉTRICAS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Precio medio", f"{df_filtrado['price'].mean():.0f}€")
col2.metric("Alojamientos", df_filtrado.shape[0])
col3.metric("Barrios", df_filtrado['neighbourhood_cleansed'].nunique())
col4.metric("Puntuación media", f"{df_filtrado['review_scores_rating'].mean():.2f}")

# --- GRÁFICOS ---
col_a, col_b = st.columns(2)

with col_a:
    st.header("Precio por barrio")
    precio_por_barrio = df_filtrado.groupby('neighbourhood_cleansed')['price'].mean().sort_values(ascending=False).head(15)
    fig = px.bar(
        precio_por_barrio,
        orientation='h',
        labels={'value': 'Precio medio (€)', 'index': 'Barrio'},
        color=precio_por_barrio.values,
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#cccccc',
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.header("Tipo de alojamiento")
    precio_por_tipo = df_filtrado.groupby('room_type')['price'].mean().sort_values(ascending=False).reset_index()
    fig2 = px.bar(
        precio_por_tipo,
        x='room_type',
        y='price',
        labels={'room_type': 'Tipo', 'price': 'Precio medio (€)'},
        color='price',
        color_continuous_scale='Reds'
    )
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#cccccc',
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    st.header("Barrios más ocupados")
    ocupacion = df_filtrado.groupby('neighbourhood_cleansed').agg(
        reseñas_media=('number_of_reviews', 'mean')
    ).sort_values('reseñas_media', ascending=False).head(15)
    fig3 = px.bar(
        ocupacion,
        orientation='h',
        labels={'value': 'Media de reseñas', 'index': 'Barrio'},
        color=ocupacion.values.flatten(),
        color_continuous_scale='Reds'
    )
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#cccccc',
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.header("Precio vs Puntuación")
    df_clean = df_filtrado.dropna(subset=['review_scores_rating'])
    fig4 = px.scatter(
        df_clean,
        x='price',
        y='review_scores_rating',
        labels={'price': 'Precio por noche (€)', 'review_scores_rating': 'Puntuación'},
        opacity=0.4,
        color='room_type',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#cccccc',
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig4, use_container_width=True)

# --- INSIGHTS ---
st.header("Conclusiones")

insights = [
    "<strong>Diagonal Mar</strong> lidera en precio medio general, pero al filtrar por apartamentos enteros <strong>Dreta de l'Eixample</strong> toma el primer puesto — Diagonal Mar concentra más hoteles que inflan su media.",
    "Los <strong>apartamentos enteros</strong> representan el 68% de la oferta y tienen el precio medio más alto, muy por encima de habitaciones privadas y compartidas.",
    "<strong>Camp d'en Grassot i Gràcia Nova</strong> es el barrio más ocupado pese a no ser de los más caros, reflejando una alta demanda de experiencias locales y auténticas.",
    "Existe una <strong>correlación positiva débil</strong> entre precio y puntuación. Pagar más tiende a garantizar buenas valoraciones, pero la puntuación se estabiliza cerca del máximo independientemente del precio.",
    "El precio medio real tras eliminar outliers es de <strong>160€/noche</strong>, muy por debajo del máximo de 10.000€ que distorsionaba el análisis inicial."
]

for insight in insights:
    st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)