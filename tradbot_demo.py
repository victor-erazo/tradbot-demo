import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import os

# Configuración de página
st.set_page_config(page_title="Tradbot PRO", layout="wide")

# Cargar logo
logo_path = "assets/tradbot_logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=200)

st.title("🤖 Tradbot PRO – Análisis Técnico y Fundamental")

# Selección de activo y parámetros
activos = {
    "ECOPETROL (EC)": "EC",
    "BITCOIN (BTC-USD)": "BTC-USD",
    "PFAVAL (BVC simulada)": "PFAVAL.BOG",
    "ISA (BVC simulada)": "ISA.BOG",
    "ETFs SPY": "SPY"
}

activo_nombre = st.selectbox("Selecciona un activo:", list(activos.keys()))
activo = activos[activo_nombre]
periodo = st.selectbox("Periodo histórico", ["1mo", "3mo", "6mo", "1y", "2y"])
mostrar_sma = st.checkbox("Mostrar SMA 20")
mostrar_ema = st.checkbox("Mostrar EMA 20")
mostrar_rsi = st.checkbox("Mostrar RSI")

# Obtener datos
data = yf.Ticker(activo)
hist = data.history(period=periodo)
hist["SMA_20"] = hist["Close"].rolling(window=20).mean()
hist["EMA_20"] = hist["Close"].ewm(span=20, adjust=False).mean()
delta = hist["Close"].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
hist["RSI"] = 100 - (100 / (1 + rs))

# Panel de métricas
st.subheader(f"📊 Datos recientes de {activo_nombre}")
precio_actual = hist["Close"].iloc[-1]
variacion = hist["Close"].iloc[-1] - hist["Close"].iloc[-2]
porcentaje = (variacion / hist["Close"].iloc[-2]) * 100
col1, col2, col3 = st.columns(3)
col1.metric("Precio actual", f"${precio_actual:.2f}")
col2.metric("Variación diaria", f"${variacion:.2f}")
col3.metric("Cambio %", f"{porcentaje:.2f}%")

# Gráfico técnico
st.subheader("📈 Gráfico con indicadores técnicos")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(hist.index, hist["Close"], label="Precio Cierre", linewidth=2)
if mostrar_sma:
    ax.plot(hist.index, hist["SMA_20"], label="SMA 20", linestyle="--")
if mostrar_ema:
    ax.plot(hist.index, hist["EMA_20"], label="EMA 20", linestyle=":")
ax.set_title(f"{activo_nombre} - Histórico de precios")
ax.set_ylabel("Precio USD")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# RSI opcional
if mostrar_rsi:
    st.subheader("📉 RSI (Índice de Fuerza Relativa)")
    fig2, ax2 = plt.subplots(figsize=(10, 2))
    ax2.plot(hist.index, hist["RSI"], label="RSI", color="purple")
    ax2.axhline(70, color="red", linestyle="--")
    ax2.axhline(30, color="green", linestyle="--")
    ax2.set_title("RSI (14 días)")
    ax2.grid(True)
    st.pyplot(fig2)

# Panel de análisis fundamental básico
st.subheader("📚 Análisis fundamental")
info = data.info
colf1, colf2, colf3 = st.columns(3)
colf1.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,}")
colf2.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
colf3.metric("Dividend Yield", f"{round(info.get('dividendYield', 0)*100, 2)}%")

st.markdown("**Sector**: " + str(info.get('sector', 'N/A')))
st.markdown("**Industria**: " + str(info.get('industry', 'N/A')))
st.markdown("**Descripción**: " + str(info.get('longBusinessSummary', 'N/A'))[:400] + "...")

# Simulador de inversión
st.subheader("💸 Simulador de inversión")
monto = st.number_input("Monto hipotético (USD)", value=1000)
fecha_inicio = st.date_input("Fecha de compra simulada", value=hist.index[0].date())
if str(fecha_inicio) in hist.index.astype(str).tolist():
    precio_inicio = hist.loc[str(fecha_inicio), "Close"]
    ganancia = ((precio_actual - precio_inicio) / precio_inicio) * monto
    st.success(f"Habrías ganado/perdido: ${ganancia:,.2f}")
else:
    st.warning("No hay datos exactos para la fecha seleccionada.")

# Captura de correos
st.subheader("🔔 ¿Quieres recibir señales premium?")
correo = st.text_input("Ingresa tu correo para recibir alertas")
if correo:
    st.success("¡Gracias! Te notificaremos con señales y análisis.")

st.caption("Tradbot PRO – v1.0 – Datos vía Yahoo Finance")
