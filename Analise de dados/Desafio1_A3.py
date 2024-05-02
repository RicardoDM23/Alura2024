"""
Que tal praticar a criação de um gráfico de linha com a 
biblioteca Plotly Express? 
Você pode usar os dados da planilha e tentar criar um 
gráfico de linha que mostre a variação do valor das ações ao 
longo do tempo. Isso pode ser feito usando a função px.line 
do Plotly Express. Experimente e veja como se sai!
"""

import pandas as pd
import plotly.express as px

df_principal = pd.read_excel("Analise de dados/acoes.xlsx",sheet_name="Principal")
print(df_principal)

df_total_acoes = pd.read_excel("Analise de dados/acoes.xlsx",sheet_name="Total_de_acoes")
print(df_total_acoes)

pd.options.display.float_format = '{:.2f}'.format

df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()
df_principal = df_principal.rename(columns={'Último (R$)':'valor_final', 'Var. Dia (%)':'var_dia_pct'}).copy()
df_total_acoes = df_total_acoes.rename(columns={'Código':'Codigo', 'Qtde. Teórica':'qtde_teorica'}).copy()
df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Codigo', how='left')
df_principal = df_principal.drop(columns=['Codigo'])
df_principal['Var_pct_dia'] = df_principal['var_dia_pct']/100
df_principal['valor_inicial_dia'] = df_principal['valor_final']/(1 + df_principal['Var_pct_dia'])
df_principal['Variacao_rs_dia'] = (df_principal['valor_final'] - df_principal['valor_inicial_dia']) * df_principal['qtde_teorica']
df_principal['Resultado_dia'] = df_principal['Variacao_rs_dia'].apply(lambda x: 'Subiu' if x > 0 else
                                                                      ('Desceu' if x < 0 else 'Estavel'))
df_principal['Variacao_rs_dia'] = (df_principal['valor_final'] - df_principal['valor_inicial_dia']) * df_principal['qtde_teorica']

print(df_principal)

df_analise = df_principal[['Ativo','Data','valor_final','var_dia_pct']].copy()
fig = px.line(df_analise,y='valor_final',x='Ativo',text='var_dia_pct', title='Line Ativo x Valor Final')
fig.show()