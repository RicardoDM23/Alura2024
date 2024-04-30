import pandas as pd

df_principal = pd.read_excel('Analise de dados/acoes.xlsx',sheet_name="Principal")
print(df_principal)

df_total_acoes = pd.read_excel("Analise de dados/acoes.xlsx",sheet_name="Total_de_acoes")
print(df_total_acoes)

df_ticker = pd.read_excel("Analise de dados/acoes.xlsx",sheet_name="Ticker")
print(df_ticker)
