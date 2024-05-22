import pandas as pd
import os


# Informar o código da UGMT ########################

codigo_ugmt = 3013983346

####################################################

def criar_estrutura_diretorios(codigo_ugmt):
    base_dir = f"UGMT_{codigo_ugmt}"
    subdirs = ["DSS_Figuras", "DSS_Loadshapes"]

    try:
        # Cria o diretório base
        os.makedirs(base_dir, exist_ok=True)

        # Cria os subdiretórios
        for subdir in subdirs:
            os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)

        print(f"Estrutura de diretórios para UGMT_{codigo_ugmt} criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar estrutura de diretórios: {e}")

criar_estrutura_diretorios(codigo_ugmt)


#### Geração do arquivo csv com os dados da UGMT
def filtrar_dados_por_codigo(codigo_ugmt):
    # Lê o arquivo CSV
    df = pd.read_csv('KW_UGMTS_CEMIG.csv')

    # Filtra os dados pelo código fornecido
    df_filtrado = df[df['UGMT'] == codigo_ugmt]

    # Grava os dados filtrados em um novo arquivo CSV
    df_filtrado.to_csv(f'{codigo_ugmt}.csv', index=False)
    # Salva o DataFrame em um arquivo Excel

    print(f'Arquivo criado com sucesso.')

filtrar_dados_por_codigo(codigo_ugmt)
