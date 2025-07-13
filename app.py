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

st.title("📚 Dashboard – Libros más vendidos en Amazon (2009–2019)")
st.markdown("Visualización de datos basada en 3 hipótesis extraídas del análisis histórico del top 50 de Amazon.")

# H1: Precio vs Calificación
st.subheader("📉 Hipótesis 1: Los libros más baratos tienden a recibir mejores calificaciones")
fig1, ax1 = plt.subplots()
sns.regplot(data=filtered_df, x="Price", y="User Rating", scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=ax1)
ax1.set_title("Relación entre Precio y Calificación")
st.pyplot(fig1)

# H2: Calificación por Género
st.subheader("📊 Hipótesis 2: Existen géneros que siempre serán bien calificados")
fig2, ax2 = plt.subplots()
sns.boxplot(data=filtered_df, x="Genre", y="User Rating", palette="Set2", ax=ax2)
ax2.set_title("Distribución de calificaciones por género")
st.pyplot(fig2)

# H3: Calificación vs Años en ranking
st.subheader("⏱️ Hipótesis 3: Una buena calificación mantiene al libro más tiempo en el ranking")
avg_rating = df.groupby("Name").agg({"User Rating": "mean", "Appearances": "first"}).reset_index()
fig3, ax3 = plt.subplots()
sns.regplot(data=avg_rating, x="User Rating", y="Appearances", scatter_kws={"alpha": 0.5}, line_kws={"color": "green"}, ax=ax3)
ax3.set_title("Calificación promedio vs Años en ranking")
st.pyplot(fig3)

st.markdown("Fuente de datos: [Kaggle - Amazon Top 50 Books](https://www.kaggle.com/datasets/sootersaalu/amazon-top-50-bestselling-books-2009-2019)")
