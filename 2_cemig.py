import pandas as pd
import matplotlib.pyplot as plt

# Caminho do arquivo de entrada
arquivo_entrada = r'C:\pythonjr\TED_ANEEL\3013545376_OK.csv'

# Ler o arquivo CSV
df = pd.read_csv(arquivo_entrada, delimiter=';')

# Converter a segunda coluna para o formato de data/hora
df['DateTime'] = pd.to_datetime(df.iloc[:, 1], format='%d/%m/%Y %H:%M')

# Obter o nome do valor indicado na primeira coluna
nome_valor = df.iloc[0, 0]

# Plotar os valores numéricos da quarta coluna em função da data/hora da segunda coluna
plt.figure(figsize=(10, 6))
plt.plot(df['DateTime'], df.iloc[:, 3], linestyle='-')
plt.title(f'UGMT:  {nome_valor}')
plt.xlabel('Data/Hora')
plt.ylabel('Potência Injetada (kW)')
plt.grid(True, linestyle=':', color='lightgrey')
plt.tight_layout()
plt.show()
