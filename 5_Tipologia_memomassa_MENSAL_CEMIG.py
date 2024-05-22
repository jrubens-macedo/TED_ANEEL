import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

import warnings
warnings.filterwarnings('ignore')

# Selecione a UGMT desejada ###########

cod_ugmt = 3013983346

#######################################

# Nome do arquivo de dados
nome_arquivo = fr'C:\pythonjr\tedaneel\{cod_ugmt}.csv'


###########################################################
# ESCOLHA DO MÊS
###########################################################

mes_escolhido = 1

###########################################################

# Dicionário de abreviações de meses em português
meses_abreviados = {
    1: "JAN",
    2: "FEV",
    3: "MAR",
    4: "ABR",
    5: "MAI",
    6: "JUN",
    7: "JUL",
    8: "AGO",
    9: "SET",
    10: "OUT",
    11: "NOV",
    12: "DEZ"
}

# Verifica se o mês escolhido é válido e atribui a abreviação correspondente
if 1 <= mes_escolhido <= 12:
    mes_selecionado = meses_abreviados[mes_escolhido]
    print(f"Mês selecionado............: {mes_selecionado}")
else:
    print("Número do mês inválido. Por favor, insira um valor entre 1 e 12.")


# Extrair o nome do arquivo da parte final do caminho
mes_csv = os.path.basename(nome_arquivo)
# Remover a extensão ".csv" se presente
mes_ugmt = os.path.splitext(mes_csv)[0]
print(mes_ugmt)

try:
    # Listas para armazenar os dados
    data_hora_lista = []
    kw_lista = []

    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        cabeçalho = next(leitor_csv, None)
        ultima_linha = None

        for linha in leitor_csv:
            ultima_linha = linha  # Atualiza a ultima_linha a cada iteração para que ao final contenha a última linha do arquivo
            data_hora_str = linha[1]
            data_hora = datetime.strptime(data_hora_str, '%d/%m/%Y %H:%M')

            # Definir o começo do intervalo de análise
            primeiro_dia = datetime(data_hora.year, mes_escolhido, 1, 1)
            # Definir o fim do intervalo de análise, 00:00:00 do primeiro dia do mês seguinte
            if mes_escolhido == 12:
                ultimo_dia = datetime(data_hora.year + 1, 1, 1)  # Ano seguinte, janeiro, meia-noite
            else:
                ultimo_dia = datetime(data_hora.year, mes_escolhido + 1, 1, 1)  # Próximo mês, meia-noite

            # Filtro para incluir dados do intervalo [primeiro_dia, ultimo_dia)
            if primeiro_dia <= data_hora < ultimo_dia:
                kw = float(linha[3])
                data_hora_lista.append(data_hora)
                kw_lista.append(kw)

    df = pd.DataFrame({'Data/Hora': data_hora_lista, 'kw': kw_lista})

    # Adiciona a última linha do arquivo ao DataFrame se mes_escolhido for Dezembro
    if mes_escolhido == 12 and ultima_linha:
        ultima_data_hora = datetime.strptime(ultima_linha[1], '%d/%m/%Y %H:%M')
        ultima_kw = float(ultima_linha[3])
        ultima_df = pd.DataFrame({'Data/Hora': [ultima_data_hora], 'kw': [ultima_kw]})
        df = pd.concat([df, ultima_df], ignore_index=True)

    print("DataFrame para o mês selecionado:")
    print(df)

# Filtra os registros associados a dias úteis
    df_DU_absoluto = df[df['Data/Hora'].dt.weekday < 5]

    # Filtra os registros associados a domingos
    df_DO_absoluto = df[df['Data/Hora'].dt.weekday == 6]

    # Filtra os registros associados a sábados
    df_SA_absoluto = df[df['Data/Hora'].dt.weekday == 5]

    # Calcula o máximo valor de kW em df_SU (bases dos Loadshpaes)
    max_kW_DU = df_DU_absoluto['kw'].max()
    max_kW_SA = df_SA_absoluto['kw'].max()
    max_kW_DO = df_DO_absoluto['kw'].max()

    # Cria um DataFrame DU com os dados normalizados
    df_DU = df_DU_absoluto.copy()
    df_DU['kw'] = df_DU['kw'] / max_kW_DU

    # Cria um DataFrame SA com os dados normalizados
    df_SA = df_SA_absoluto.copy()
    df_SA['kw'] = df_SA['kw'] / max_kW_SA

    # Cria um DataFrame DO com os dados normalizados
    df_DO = df_DO_absoluto.copy()
    df_DO['kw'] = df_DO['kw'] / max_kW_DO


    # Configuração do layout dos subplots
    plt.figure(figsize=(18, 6))

    # Subplot para DIAS ÚTEIS
    plt.subplot(1, 3, 1)

    for _, grupo in df_DU.groupby(df_DU['Data/Hora'].dt.date):
        plt.plot(grupo['Data/Hora'].dt.hour, grupo['kw'], label=grupo['Data/Hora'].iloc[0].strftime('%Y-%m-%d'))

    # Calcula a média para cada hora do dia em DIAS ÚTEIS
    media_DU = df_DU.groupby(df_DU['Data/Hora'].dt.hour)['kw'].mean()
    plt.plot(media_DU.index, media_DU, label='Média DIAS ÚTEIS', color='black', linestyle='-', linewidth=3)

    # Adiciona o valor de max_kW_DU no gráfico
    plt.text(0.183, 0.88, f'Máx. kW (DU) = {max_kW_DU:.2f} kW', transform=plt.gcf().transFigure,
             horizontalalignment='center', verticalalignment='center',
             bbox=dict(facecolor='white', edgecolor='white'), fontweight='bold', fontsize=12)
    plt.text(0.183, 0.84, f'(Mês {mes_escolhido})  UGMT = {mes_ugmt}', transform=plt.gcf().transFigure,
             horizontalalignment='center', verticalalignment='center',
             bbox=dict(facecolor='white', edgecolor='white'), fontweight='bold', fontsize=12)

    plt.title('DIAS ÚTEIS (DU)', fontsize=17)
    plt.xlabel('Hora do Dia', fontsize=16)
    plt.ylabel('Potência Ativa (pu)', fontsize=16)
    plt.grid(True, linestyle='dotted', alpha=0.7)
    plt.ylim(0, 1.2)
    plt.xlim(-0.5, 24)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Subplot para SÁBADOS
    plt.subplot(1, 3, 2)

    for _, grupo in df_SA.groupby(df_SA['Data/Hora'].dt.date):
        plt.plot(grupo['Data/Hora'].dt.hour, grupo['kw'], label=grupo['Data/Hora'].iloc[0].strftime('%Y-%m-%d'))

    # Calcula a média para cada hora do dia em SÁBADOS
    media_SA = df_SA.groupby(df_SA['Data/Hora'].dt.hour)['kw'].mean()
    plt.plot(media_SA.index, media_SA, label='Média SÁBADOS', color='black', linestyle='-', linewidth=3)

    # Adiciona o valor de max_kW_DU no gráfico
    plt.text(0.51, 0.88, f'Máx. kW (SA) = {max_kW_SA:.2f} kW', transform=plt.gcf().transFigure,
             horizontalalignment='center', verticalalignment='center',
             bbox=dict(facecolor='white', edgecolor='white'), fontweight='bold', fontsize=12)
    plt.text(0.51, 0.84, f'(Mês {mes_escolhido})  UGMT = {mes_ugmt}', transform=plt.gcf().transFigure,
             horizontalalignment='center', verticalalignment='center',
             bbox=dict(facecolor='white', edgecolor='white'), fontweight='bold', fontsize=12)

    plt.title('SÁBADOS (SA)', fontsize=17)
    plt.xlabel('Hora do Dia', fontsize=16)
    plt.ylabel('Potência Ativa (pu)', fontsize=16)
    plt.grid(True, linestyle='dotted', alpha=0.7)
    plt.ylim(0, 1.2)
    plt.xlim(-0.5, 24)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Subplot para DOMINGOS
    plt.subplot(1, 3, 3)

    for _, grupo in df_DO.groupby(df_DO['Data/Hora'].dt.date):
        plt.plot(grupo['Data/Hora'].dt.hour, grupo['kw'], label=grupo['Data/Hora'].iloc[0].strftime('%Y-%m-%d'))

    # Calcula a média para cada hora do dia em DOMINGOS
    media_DO = df_DO.groupby(df_DO['Data/Hora'].dt.hour)['kw'].mean()
    plt.plot(media_DO.index, media_DO, label='Média DOMINGOS', color='black', linestyle='-', linewidth=3)

    # Adiciona o valor de max_kW_DO no gráfico
    plt.text(0.828, 0.88, f'Máx. kW (DO) = {max_kW_DO:.2f} kW', transform=plt.gcf().transFigure,
             horizontalalignment='center', verticalalignment='center',
             bbox=dict(facecolor='white', edgecolor='white'), fontweight='bold', fontsize=12)
    plt.text(0.828, 0.84, f'(Mês {mes_escolhido})  UGMT = {mes_ugmt}', transform=plt.gcf().transFigure,
             horizontalalignment='center', verticalalignment='center',
             bbox=dict(facecolor='white', edgecolor='white'), fontweight='bold', fontsize=12)

    plt.title('DOMINGOS (DO)', fontsize=17)
    plt.xlabel('Hora do Dia', fontsize=16)
    plt.ylabel('Potência Ativa (pu)', fontsize=16)
    plt.grid(True, linestyle='dotted', alpha=0.7)
    plt.ylim(0, 1.2)
    plt.xlim(-0.5, 24)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Ajusta o layout para evitar sobreposição
    plt.tight_layout()

    # Caminho para salvar o gráfico
    caminho_figura = fr'C:\pythonjr\tedaneel\UGMT_{cod_ugmt}\DSS_Figuras\UGMT_{cod_ugmt}_{mes_selecionado}.png'

    # Salvar o gráfico
    plt.savefig(caminho_figura)

    plt.show()

    # Criando um objeto ExcelWriter
    with pd.ExcelWriter(fr'C:\pythonjr\tedaneel\UGMT_{cod_ugmt}\output.xlsx') as writer:

        # Escrevendo a aba de Dias Úteis
        df_DU_pivot = df_DU.pivot_table(index=df_DU['Data/Hora'].dt.hour, columns=df_DU['Data/Hora'].dt.date, values='kw', aggfunc='sum')
        df_DU_pivot.to_excel(writer, sheet_name='DU')

        # Escrevendo a aba de Sábados
        df_SA_pivot = df_SA.pivot_table(index=df_SA['Data/Hora'].dt.hour, columns=df_SA['Data/Hora'].dt.date, values='kw', aggfunc='sum')
        df_SA_pivot.to_excel(writer, sheet_name='SA')

        # Escrevendo a aba de Domingos
        df_DO_pivot = df_DO.pivot_table(index=df_DO['Data/Hora'].dt.hour, columns=df_DO['Data/Hora'].dt.date, values='kw', aggfunc='sum')
        df_DO_pivot.to_excel(writer, sheet_name='DO')

    print("#### Arquivo .xlsx criado com sucesso ####")

    # Criar array formatado com os valores de media_DO
    array_media_DU = np.round(np.array(media_DU), 4)
    array_media_SA = np.round(np.array(media_SA), 4)
    array_media_DO = np.round(np.array(media_DO), 4)

    # Salvar array em um arquivo de texto (.dss)
    with open(fr'C:\pythonjr\tedaneel\UGMT_{cod_ugmt}\DSS_Loadshapes\UGMT_{cod_ugmt}_{mes_selecionado}.dss', 'w') as arquivo_dss:
        arquivo_dss.write(f'{mes_ugmt}\n')
        arquivo_dss.write(f'Max_kW_DU = {max_kW_DU}\n')
        arquivo_dss.write(f'Max_kW_SA = {max_kW_SA}\n')
        arquivo_dss.write(f'Max_kW_DO = {max_kW_DO}\n')
        arquivo_dss.write(f'----------------------------------------\n')
        arquivo_dss.write(
            f'New "Loadshape.UGMT_DU" {len(array_media_DU)} 1.0 mult=({" ".join(map(str, array_media_DU))})\n')
        arquivo_dss.write(
            f'New "Loadshape.UGMT_SA" {len(array_media_SA)} 1.0 mult=({" ".join(map(str, array_media_SA))})\n')
        arquivo_dss.write(
            f'New "Loadshape.UGMT_DO" {len(array_media_DO)} 1.0 mult=({" ".join(map(str, array_media_DO))})\n')

    print(f'#### Arquivo .dss criado com sucesso #### ')

except FileNotFoundError:
    print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

