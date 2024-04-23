import pandas as pd


def filtrar_dados_por_codigo(codigo):
    # Lê o arquivo CSV
    df = pd.read_csv('CEMIG_UGMT_2021_1MW.csv')

    # Filtra os dados pelo código fornecido
    df_filtrado = df[df['CodGeraMT'] == codigo]

    # Grava os dados filtrados em um novo arquivo CSV
    df_filtrado.to_csv(f'filtrado_{codigo}.csv', index=False)
    # Salva o DataFrame em um arquivo Excel

    print(f'Arquivo criado com sucesso.')


# Solicitar o código ao usuário
codigo = 3013983346
filtrar_dados_por_codigo(codigo)
