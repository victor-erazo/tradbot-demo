
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import numpy as np

# -------- FUNCIONES -----------
def obtener_precio_ecopetrol_bvc():
    url = "https://www.investing.com/equities/ecopetrol"
    headers = { "User-Agent": "Mozilla/5.0" }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        precio = soup.find("span", {"data-test": "instrument-price-last"}).text.strip()
        variacion = soup.find("span", {"data-test": "instrument-price-change-percent"}).text.strip()
        return precio, variacion
    except Exception as e:
        return "Error", str(e)

def simular_datos_historicos(dias=60, precio_inicial=2500):
    fechas = [datetime.now() - timedelta(days=i) for i in range(dias)][::-1]
    precios = [precio_inicial + np.random.normal(0, 20) for _ in range(dias)]
    df = pd.DataFrame({'Fecha': fechas, 'Precio': precios})
    df['SMA_10'] = df['Precio'].rolling(window=10).mean()
    df['EMA_10'] = df['Precio'].ewm(span=10, adjust=False).mean()
    return df

# -------- APP STREAMLIT -----------
st.set_page_config(page_title="Tradbot - Demo ECOPETROL", layout="wide")

# Logo
from PIL import Image
logo = Image.open("assets/tradbot_logo.png")
st.image(logo, width=220)

st.title("📊 Tradbot - Seguimiento ECOPETROL:BVC")

# Mostrar datos actuales
st.subheader("📌 Precio actual en Bolsa de Valores de Colombia")
precio, variacion = obtener_precio_ecopetrol_bvc()
st.metric(label="ECOPETROL:BVC", value=precio, delta=variacion)

# Simulación de datos históricos
st.subheader("📈 Evolución histórica simulada y análisis técnico")

df = simular_datos_historicos()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df['Fecha'], df['Precio'], label="Precio", linewidth=2)
ax.plot(df['Fecha'], df['SMA_10'], label="SMA 10 días", linestyle='--')
ax.plot(df['Fecha'], df['EMA_10'], label="EMA 10 días", linestyle='-.')
ax.set_title("Simulación histórica ECOPETROL:BVC")
ax.set_ylabel("COP")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Footer
st.caption("Versión Demo Tradbot | Datos locales de ECOPETROL:BVC simulados y reales | Powered by Streamlit")
