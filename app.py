import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Colores definidos
COLOR_PUNTOS = "#1f77b4"
COLOR_LINEA = "#17becf"
COLOR_CAJAS = "#545C80"

# Estilo uniforme
sns.set_style("whitegrid")
plt.rcParams.update({
    "axes.edgecolor": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black"
})

# Cargar datos
df = pd.read_csv("bestsellers_with_categories.csv")
df.drop_duplicates(inplace=True)
df["Appearances"] = df.groupby("Name")["Year"].transform("count")

# Sidebar
st.sidebar.title("Filtros")
selected_year = st.sidebar.selectbox("Año", ["Todos"] + sorted(df["Year"].unique().tolist()))
selected_genre = st.sidebar.selectbox("Género", ["Todos", "Fiction", "Non Fiction"])

filtered_df = df.copy()
if selected_year != "Todos":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]
if selected_genre != "Todos":
    filtered_df = filtered_df[filtered_df["Genre"] == selected_genre]

# Título principal
st.title("Dashboard – Libros más vendidos en Amazon (2009–2019)")
st.markdown("Visualización basada en 3 hipótesis clave.")

# Columnas principales
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Hipótesis 1: Precio vs Calificación")
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    sns.regplot(
        data=filtered_df, x="Price", y="User Rating",
        scatter_kws={"alpha": 0.6, "color": COLOR_PUNTOS},
        line_kws={"color": COLOR_LINEA}, ax=ax1
    )
    ax1.set_title("Relación entre Precio y Calificación", fontsize=12)
    st.pyplot(fig1)

with col2:
    st.subheader("Hipótesis 2: Calificación por Género")
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    sns.boxplot(
        data=filtered_df, x="Genre", y="User Rating",
        color=COLOR_CAJAS, width=0.5, fliersize=3, ax=ax2
    )
    ax2.set_title("Distribución de calificaciones por género", fontsize=12)
    st.pyplot(fig2)

# Hipótesis 3 abajo
st.subheader("Hipótesis 3: Calificación promedio vs Años en ranking")
avg_rating = df.groupby("Name").agg({
    "User Rating": "mean", "Appearances": "first"
}).reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.regplot(
    data=avg_rating, x="User Rating", y="Appearances",
    scatter_kws={"alpha": 0.6, "color": COLOR_PUNTOS},
    line_kws={"color": COLOR_LINEA}, ax=ax3
)
ax3.set_title("Relación entre calificación promedio y años en ranking", fontsize=12)
st.pyplot(fig3)

st.markdown("**Fuente de datos:** [Kaggle - Amazon Top 50 Books](https://www.kaggle.com/datasets/sootersaalu/amazon-top-50-bestselling-books-2009-2019)")
