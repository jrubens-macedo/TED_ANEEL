import pandas as pd

# Carrega o arquivo Excel
df = pd.read_excel('CEMIG_UGMT_2021_1MW_OK.xlsx', dtype={'Coluna1': str, 'Coluna4': float, 'Coluna5': float, 'Coluna6': float})

# Formata a data
df['Data'] = pd.to_datetime(df.iloc[:, 1]).dt.strftime('%d/%m/%Y')  # Formata a data como dd/mm/aaaa

# Converte a coluna de horas, assumindo que os valores representam horas completas
df['Hora'] = df.iloc[:, 2].apply(lambda x: f"{int(x):02d}:00")

# Cria uma nova coluna 'Data_Hora' combinando as colunas 'Data' e 'Hora'
df['Data_Hora'] = df['Data'] + ' ' + df['Hora']

# Seleciona as colunas necessárias, excluindo a coluna 'Hora'
df_final = df.iloc[:, [0, -1, 3, 4, 5]].copy()
df_final.columns = ['UGMT', 'Data_Hora', 'Consumo (kW)', 'Injeção (kW)', 'Potência Instalada (kW)']

# Salva o DataFrame em um arquivo CSV
df_final.to_csv('arquivo_ajustado.csv', index=False)

print("Arquivo CSV criado com sucesso!")

