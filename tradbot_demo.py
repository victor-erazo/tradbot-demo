
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title='Tradbot Demo', layout='wide')
st.title('📈 Tradbot Demo - ECOPETROL')

# Simulación de precios
np.random.seed(42)
precios = np.cumsum(np.random.randn(100)) + 3000
df = pd.DataFrame(precios, columns=['Precio'])

# Indicadores
df['SMA_10'] = df['Precio'].rolling(window=10).mean()
df['SMA_20'] = df['Precio'].rolling(window=20).mean()

# Gráfico
st.subheader('Precio de ECOPETROL con Medias Móviles')
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['Precio'], label='Precio', linewidth=1.5)
ax.plot(df['SMA_10'], label='SMA 10', linestyle='--')
ax.plot(df['SMA_20'], label='SMA 20', linestyle='--')
ax.legend()
ax.set_xlabel('Días')
ax.set_ylabel('Precio')
st.pyplot(fig)

st.markdown('👉 Esta es una versión demostrativa. Para señales en tiempo real, alertas y personalización, accede a la versión premium de **Tradbot**.')
