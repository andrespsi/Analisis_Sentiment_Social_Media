import streamlit as st
import pandas as pd
import plotly.express as px
from src.core.database import DatabaseManager

st.set_page_config(layout="wide")
st.title("📊 Dashboard de Análisis de Sentimiento")

# Conectar a la base de datos
db = DatabaseManager()
datos = db.obtener_todos_los_analisis()

if not datos:
    st.warning("No hay datos en la base de datos para mostrar. Ejecuta un análisis primero desde 'run_analysis.py'.")
else:
    # Convertir a DataFrame de Pandas para fácil manipulación
    columnas = ["ID", "Fuente", "Texto", "Sentimiento", "Confianza", "Fecha"]
    df = pd.DataFrame(datos, columns=columnas)

    # --- Fila de KPIs ---
    st.header("Resumen General")
    total_comentarios = len(df)
    sent_positivo = len(df[df["Sentimiento"] == "POS"])
    sent_negativo = len(df[df["Sentimiento"] == "NEG"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Comentarios", f"{total_comentarios}")
    col2.metric("Comentarios Positivos", f"{sent_positivo}", f"{round((sent_positivo/total_comentarios)*100, 1)}%")
    col3.metric("Comentarios Negativos", f"{sent_negativo}", f"-{round((sent_negativo/total_comentarios)*100, 1)}%")

    # --- Gráficos ---
    st.header("Visualización de Datos")
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        # Gráfico de Pastel
        fig_pie = px.pie(df, names='Sentimiento', title='Distribución de Sentimientos',
                         color='Sentimiento',
                         color_discrete_map={'POS':'green', 'NEG':'red', 'NEU':'grey'})
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_graf2:
        # Gráfico de Líneas (evolución en el tiempo)
        df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
        sent_por_dia = df.groupby(['Fecha', 'Sentimiento']).size().reset_index(name='Cantidad')
        fig_line = px.line(sent_por_dia, x='Fecha', y='Cantidad', color='Sentimiento',
                           title='Evolución de Sentimientos por Día',
                           color_discrete_map={'POS':'green', 'NEG':'red', 'NEU':'grey'})
        st.plotly_chart(fig_line, use_container_width=True)

    # --- Tabla de Datos Crudos ---
    st.header("Comentarios Recientes")
    st.dataframe(df[["Fecha", "Texto", "Sentimiento", "Confianza", "Fuente"]], use_container_width=True)