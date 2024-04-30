# Aula 3 - Importação
import pandas as pd
import plotly.express as px

df_principal = pd.read_excel("/content/acoes_pura.xlsx",sheet_name="Principal")
df_principal

df_total_acoes = pd.read_excel("/content/acoes_pura.xlsx",sheet_name="Total_de_acoes")
df_total_acoes

df_ticker = pd.read_excel("/content/acoes_pura.xlsx",sheet_name="Ticker")
df_ticker

df_chatGPT = pd.read_excel("/content/acoes_pura.xlsx",sheet_name="chatGPT")
df_chatGPT

# Recria df_principal apenas com as colunas selecionadas
df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()
df_principal

# Renomear colunas para remover pontos acentos e outros simbolos que podem causar problemas no codigo
df_principal = df_principal.rename(columns={'Último (R$)': 'valor_final', 'Var. Dia (%)':'var_dia_pct'}).copy()
df_principal

df_total_acoes = df_total_acoes.rename(columns={'Código':'Codigo','Qtde. Teórica':'qtde_teorica'})
df_total_acoes

# juntando duas tabela informando que a principal é a esquerda e vai apenas juntar as informaçoes da tabela direita (a quantidade teoria) na tabela principal
df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Codigo', how='left')
df_principal

df_principal = df_principal.drop(columns=['Codigo'])
df_principal

# agora buscando o nome da empresa
df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal = df_principal.drop(columns=['Ticker'])
df_principal

# Refazer passos feito no excell
df_principal['Var_pct_dia'] = df_principal['var_dia_pct']/100
df_principal['valor_inicial_dia'] = df_principal['valor_final']/ (1 + df_principal['Var_pct_dia'])
df_principal

df_principal['Variacao_rs_dia'] = (df_principal['valor_final'] - df_principal['valor_inicial_dia'] ) * df_principal['qtde_teorica']
df_principal

df_principal['Resultado_dia'] = df_principal['Variacao_rs_dia'].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estavel'))
df_principal

# Ajustando visualizacao dos valores
pd.options.display.float_format = '{:.2f}'.format
df_principal

df_principal['qtde_teorica'] = df_principal['qtde_teorica'].astype(int)
df_principal

# ultima etapa
df_principal = df_principal.merge(df_chatGPT, left_on='Nome', right_on='Empresa', how='left')
df_principal = df_principal.drop(columns='Nome')
df_principal

# Analises
# Maior valor de variação do Dia
maior_valor = df_principal['Variacao_rs_dia'].max()

# Menor valor de variação do Dia
menor_valor = df_principal['Variacao_rs_dia'].min()

# Média Dia
media_dia = df_principal['Variacao_rs_dia'].mean()

# Média Dia quem Subiu
media_subiu = df_principal[df_principal['Resultado_dia'] == 'Subiu']['Variacao_rs_dia'].mean()

# Média Dia quem Desceu
media_desceu = df_principal[df_principal['Resultado_dia'] == 'Desceu']['Variacao_rs_dia'].mean()

# Exibindo os resultados
print(f"Maior Dia:\tRS {maior_valor:,.2f}")
print(f"Menor Dia:\tRS {menor_valor:,.2f}")
print(f"Média Dia:\tRS {media_dia:,.2f}")
print(f"Média Dia quem Subiu:\tRS {media_subiu:,.2f}")
print(f"Média Dia quem Desceu:\tRS {media_desceu:,.2f}")

# criando df apenas com os que o resultado foi subiu
df_principal_subiu = df_principal[df_principal['Resultado_dia'] == 'Subiu']
df_principal_subiu

df_analise_segmento = df_principal_subiu.groupby('Segmento')['Variacao_rs_dia'].sum().reset_index()
df_analise_segmento

df_analise_saldo = df_principal.groupby('Resultado_dia')['Variacao_rs_dia'].sum().reset_index()
df_analise_saldo

# Criando Graficos
fig = px.bar(df_analise_saldo, x='Resultado_dia', y='Variacao_rs_dia', text='Variacao_rs_dia', title = 'Variação Reais por Resultado (DIA)')
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig.show()

fig = px.pie(df_principal_subiu, values='Variacao_rs_dia', names='Segmento', title='Variação em Reais por Segmento (DIA)')
fig.show()

df_principal_subiu