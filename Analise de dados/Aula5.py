# Ultima Aula

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet

# Baixar dados dos ultimos 4 anos para uma ação progress = false para não mostra a barra de download
dados = yf.download('JNJ', start='2020-01-01', end='2023-12-31', progress = False)
dados = dados.reset_index()

# Seprar dados de treino e dados de teste
dados_treino = dados[dados['Date'] < '2023-07-31']
dados_teste = dados[dados['Date'] >= '2023-07-31']

# Preparando dados para o Prophet as colunas deve estar nomeados como ds e y
dados_prophet_treino = dados_treino[['Date','Close']].rename(columns={'Date':'ds','Close':'y'})

# Criar o treino do modelo
modelo = Prophet(weekly_seasonality=True,
                 yearly_seasonality=True,
                 daily_seasonality=False)

modelo.add_country_holidays(country_name='US')

modelo.fit(dados_prophet_treino)

# Criar datas futuras para previsão até o final de 2023
futuro = modelo.make_future_dataframe(periods=150)
previsao = modelo.predict(futuro)

# Plotar dados de treino, teste e previsao
plt.figure(figsize = (14,8))

# x data, y close, identificaçao e cor
plt.plot(dados_treino['Date'], dados_treino['Close'], label='Dados de Treino', color='blue')
plt.plot(dados_teste['Date'], dados_teste['Close'], label='Dados Reais (Teste)', color='green')
plt.plot(previsao['ds'], previsao['yhat'], label='Previsão', color='orange', linestyle='--')

#linha vertical para separa real / previsao
plt.axvline(dados_treino['Date'].max(), color='red', linestyle='--', label='Início da Previsão')
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento')
plt.title('Previsão de Preço de Fechamento vs Dados Reais')
plt.legend()
plt.show()