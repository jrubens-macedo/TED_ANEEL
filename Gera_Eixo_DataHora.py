import pandas as pd

# Define o período do ano completo
start = '2021-01-01 01:00'
end = '2022-01-01 00:00'

# Cria um range de datas com frequência de uma hora
dates = pd.date_range(start=start, end=end, freq='h')

# Cria um DataFrame
df = pd.DataFrame(dates, columns=['Data'])

# Formata a coluna de data para o formato desejado
df['Data'] = df['Data'].dt.strftime('%d/%m/%Y %H:%M')

# Salva o DataFrame em um arquivo Excel
df.to_excel('Coluna_Data_Hora.xlsx', index=False)

