import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os

# Configuración de la página
st.set_page_config(page_title="Tradbot DEMO", layout="wide")

# Cargar el logo
logo_path = "assets/tradbot_logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=200)

st.title("📈 Tradbot DEMO – ECOPETROL (ADR) en tiempo real")

# Obtener datos de Yahoo Finance
ticker = "EC"
st.subheader(f"Datos históricos de: {ticker} (Ecopetrol NYSE)")

data = yf.Ticker(ticker)
hist = data.history(period="6mo")

# Calcular indicadores
hist["SMA_20"] = hist["Close"].rolling(window=20).mean()
hist["EMA_20"] = hist["Close"].ewm(span=20, adjust=False).mean()

# Mostrar métricas actuales
precio_actual = hist["Close"][-1]
variacion = hist["Close"][-1] - hist["Close"][-2]
porcentaje = (variacion / hist["Close"][-2]) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Precio actual", f"${precio_actual:.2f}")
col2.metric("Variación diaria", f"${variacion:.2f}")
col3.metric("Cambio %", f"{porcentaje:.2f}%")

# Mostrar gráfico
st.subheader("📊 Gráfico con SMA y EMA (20 días)")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hist.index, hist["Close"], label="Precio Cierre", linewidth=2)
ax.plot(hist.index, hist["SMA_20"], label="SMA 20", linestyle="--")
ax.plot(hist.index, hist["EMA_20"], label="EMA 20", linestyle=":")
ax.set_title("ECOPETROL (ADR) - Histórico con Indicadores")
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio USD")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.caption("Fuente: Yahoo Finance | Tradbot DEMO")