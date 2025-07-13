import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Cargar el dataset
df = pd.read_csv("bestsellers_with_categories.csv")
df.drop_duplicates(inplace=True)

# Calcular cantidad de años que aparece cada libro
df["Appearances"] = df.groupby("Name")["Year"].transform("count")

# Sidebar
st.sidebar.title("Filtros")
selected_year = st.sidebar.selectbox("Año", ["Todos"] + sorted(df["Year"].unique().tolist()))
selected_genre = st.sidebar.selectbox("Género", ["Todos", "Fiction", "Non Fiction"])

# Filtro por año y género
filtered_df = df.copy()
if selected_year != "Todos":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]
if selected_genre != "Todos":
    filtered_df = filtered_df[filtered_df["Genre"] == selected_genre]

# Título general
st.title("Dashboard – Libros más vendidos en Amazon (2009–2019)")
st.markdown("Visualización de datos basada en 3 hipótesis extraídas del análisis histórico del top 50 de Amazon.")

# Diseño en columnas más amplias para mostrar todo sin tener que bajar mucho
col1, col2 = st.columns([1, 1])  # 2 columnas iguales

with col1:
    st.subheader("Hipótesis 1: Precio vs Calificación")
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    sns.regplot(data=filtered_df, x="Price", y="User Rating", scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=ax1)
    ax1.set_title("Relación entre Precio y Calificación", fontsize=12)
    st.pyplot(fig1)

with col2:
    st.subheader("Hipótesis 2: Calificación por Género")
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=filtered_df, x="Genre", y="User Rating", palette="Set2", ax=ax2)
    ax2.set_title("Distribución de calificaciones por género", fontsize=12)
    st.pyplot(fig2)

# Debajo: gráfica 3 en pantalla completa
st.subheader("Hipótesis 3: Calificación promedio vs Años en ranking")
avg_rating = df.groupby("Name").agg({"User Rating": "mean", "Appearances": "first"}).reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.regplot(data=avg_rating, x="User Rating", y="Appearances", scatter_kws={"alpha": 0.5}, line_kws={"color": "green"}, ax=ax3)
ax3.set_title("Relación entre calificación promedio y cantidad de años en el ranking", fontsize=12)
st.pyplot(fig3)

# Fuente de datos
st.markdown("**Fuente de datos:** [Kaggle - Amazon Top 50 Books](https://www.kaggle.com/datasets/sootersaalu/amazon-top-50-bestselling-books-2009-2019)")
