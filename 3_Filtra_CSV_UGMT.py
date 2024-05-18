import pandas as pd

def filtrar_dados_por_codigo(codigo):
    # Lê o arquivo CSV
    df = pd.read_csv('KW_UGMTS_CEMIG.csv')

    # Filtra os dados pelo código fornecido
    df_filtrado = df[df['UGMT'] == codigo]

    # Grava os dados filtrados em um novo arquivo CSV
    df_filtrado.to_csv(f'filtrado_{codigo}.csv', index=False)
    # Salva o DataFrame em um arquivo Excel

    print(f'Arquivo criado com sucesso.')

# Informar o código da UGMT
#codigo = 3013983346
codigo = 3013754821

filtrar_dados_por_codigo(codigo)
