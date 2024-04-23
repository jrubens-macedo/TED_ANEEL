import pandas as pd

# Carrega o arquivo CSV
df = pd.read_csv('KW_UGMTS_CEMIG.csv')

# Certifique-se de que a coluna de interesse é a primeira coluna (índice 0)
# Se não for, ajuste o índice abaixo para corresponder à coluna correta
installation_counts = df.iloc[:, 0].value_counts().reset_index()

# Renomeia as colunas para melhor entendimento
installation_counts.columns = ['UGMT', 'Contagem de Linhas']

# Imprime as primeiras linhas para verificar os resultados
print(installation_counts.head())

# Salva o resultado em um novo arquivo CSV
installation_counts.to_csv('Resumo_UGMTs.csv', index=False)

print("Arquivo CSV com resumo das UGMTs criado com sucesso!")
