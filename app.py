import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏠 Airbnb Barcelona — Análisis de alojamientos")
st.markdown("Análisis interactivo de más de 15.000 alojamientos en Barcelona.")

df = pd.read_csv('data/listings.csv.gz', compression='gzip')

# Limpieza
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

st.sidebar.header("🔍 Filtros")

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

# Aplicar filtros
df_filtrado = df.copy()
if barrio_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['neighbourhood_cleansed'] == barrio_seleccionado]
if tipo_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['room_type'] == tipo_seleccionado]
df_filtrado = df_filtrado[(df_filtrado['price'] >= precio_min) & (df_filtrado['price'] <= precio_max)]

st.info(f"🏠 {df_filtrado.shape[0]} alojamientos con los filtros aplicados")

st.success(f"✅ {df_filtrado.shape[0]} alojamientos cargados")
st.dataframe(df_filtrado.head(10))

st.header("💰 Precio medio por barrio")

precio_por_barrio = df_filtrado.groupby('neighbourhood_cleansed')['price'].mean().sort_values(ascending=False).head(15)

fig = px.bar(
    precio_por_barrio,
    orientation='h',
    title='Top 15 barrios más caros',
    labels={'value': 'Precio medio (€)', 'index': 'Barrio'},
    color=precio_por_barrio.values,
    color_continuous_scale='Blues'
)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig, use_container_width=True)

st.header("🏨 Precio por tipo de alojamiento")

precio_por_tipo = df_filtrado.groupby('room_type')['price'].mean().sort_values(ascending=False).reset_index()

fig2 = px.bar(
    precio_por_tipo,
    x='room_type',
    y='price',
    title='Precio medio por tipo de alojamiento',
    labels={'room_type': 'Tipo', 'price': 'Precio medio (€)'},
    color='price',
    color_continuous_scale='Blues'
)
st.plotly_chart(fig2, use_container_width=True)

st.header("📊 Barrios más ocupados")

ocupacion = df_filtrado.groupby('neighbourhood_cleansed').agg(
    reseñas_media=('number_of_reviews', 'mean')
).sort_values('reseñas_media', ascending=False).head(15)

fig3 = px.bar(
    ocupacion,
    orientation='h',
    title='Top 15 barrios con más reseñas (más ocupados)',
    labels={'value': 'Media de reseñas', 'index': 'Barrio'},
    color=ocupacion.values.flatten(),
    color_continuous_scale='Greens'
)
fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig3, use_container_width=True)

st.header("⭐ Relación precio vs puntuación")

df_clean = df_filtrado.dropna(subset=['review_scores_rating'])

fig4 = px.scatter(
    df_clean,
    x='price',
    y='review_scores_rating',
    title='Precio vs Puntuación',
    labels={'price': 'Precio por noche (€)', 'review_scores_rating': 'Puntuación'},
    opacity=0.4,
    color='room_type'
)
st.plotly_chart(fig4, use_container_width=True)