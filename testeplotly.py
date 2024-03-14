import csv
from datetime import datetime
import pandas as pd
import numpy as np
import os
import plotly.graph_objs as go
import plotly.io as pio

nome_arquivo = r'C:\pythonjr\aneel\UGMT_15732740\CSVs\ANUAL_15732740.csv'

# Extrair o nome do arquivo da parte final do caminho
mes_csv = os.path.basename(nome_arquivo)
# Remover a extensão ".csv" se presente
mes_ugmt = os.path.splitext(mes_csv)[0]
print(mes_ugmt)

try:
    # Listas para armazenar os dados
    data_hora_lista = []
    kw_lista = []

    # Abre o arquivo CSV em modo de leitura
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo_csv:
        # Cria um objeto leitor CSV
        leitor_csv = csv.reader(arquivo_csv)

        # Ignora o cabeçalho se houver
        cabeçalho = next(leitor_csv, None)

        # Itera sobre as linhas do arquivo
        for linha in leitor_csv:
            # Converte os dados da primeira coluna para o formato 'dd/mm/aaaa hh:mm'
            data_hora_str = linha[0]
            data_hora = datetime.strptime(data_hora_str, '%d/%m/%Y %H:%M')

            # Converte os dados da segunda coluna para float
            kw = float(linha[1])

            # Armazena os dados nas listas
            data_hora_lista.append(data_hora)
            kw_lista.append(kw)

    # Cria um DataFrame com os dados brutos
    df = pd.DataFrame({'Data/Hora': data_hora_lista, 'kw': kw_lista})

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

    # Imprime os DataFrames
    print("DataFrame - Dias Úteis:")
    print(df_DU)
    print("DataFrame - Sábados:")
    print(df_SA)
    print("DataFrame - Domingos:")
    print(df_DO)

    # Configuração do layout dos subplots
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()


    #################################################
    # Subplot para DIAS ÚTEIS
    for _, grupo in df_DU.groupby(df_DU['Data/Hora'].dt.date):
        fig1.add_trace(go.Scatter(x=grupo['Data/Hora'].dt.hour, y=grupo['kw'], mode='lines', name=grupo['Data/Hora'].iloc[0].strftime('%Y-%m-%d')))

    # Calcula a média para cada hora do dia em DIAS ÚTEIS
    media_DU = df_DU.groupby(df_DU['Data/Hora'].dt.hour)['kw'].mean()
    fig1.add_trace(go.Scatter(x=media_DU.index, y=media_DU, mode='lines', name='Média DIAS ÚTEIS', line=dict(color='black', width=3)))

    # Adiciona o valor de max_kW_DU no gráfico
    fig1.update_layout(annotations=[
        dict(
            x=0.183,
            y=0.88,
            xref='paper',
            yref='paper',
            text=f'Máx kW (DU) = {max_kW_DU:.2f} kW\nUGMT = {mes_ugmt}',
            showarrow=False,
            bgcolor='white',
            bordercolor='white'
        )
    ])
    fig1.update_xaxes(title='Hora do Dia')
    fig1.update_yaxes(title='Potência Ativa (pu)')
    fig1.update_layout(title='ANÁLISE DIAS ÚTEIS (DU)', grid=dict(columns=1, rows=1),
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      showlegend=True)

    # Salvando a figura em HTML
    pio.write_html(fig1, r'C:\pythonjr\aneel\UGMT_15732740\grafico_DU.html')
    print("Figura DIAS ÚTEIS salva em HTML com sucesso.")

    #################################################
    # Subplot para SÁBADOS
    for _, grupo in df_SA.groupby(df_SA['Data/Hora'].dt.date):
        fig2.add_trace(go.Scatter(x=grupo['Data/Hora'].dt.hour, y=grupo['kw'], mode='lines',
                                 name=grupo['Data/Hora'].iloc[0].strftime('%Y-%m-%d')))

    # Calcula a média para cada hora do dia em SÁBADOS
    media_SA = df_SA.groupby(df_SA['Data/Hora'].dt.hour)['kw'].mean()
    fig2.add_trace(go.Scatter(x=media_SA.index, y=media_SA, mode='lines', name='Média SÁBADOS',
                             line=dict(color='black', width=3)))

    # Adiciona o valor de max_kW_xx gráfico
    fig2.update_layout(annotations=[
        dict(
            x=0.183,
            y=0.88,
            xref='paper',
            yref='paper',
            text=f'Máx kW (SA) = {max_kW_SA:.2f} kW\nUGMT = {mes_ugmt}',
            showarrow=False,
            bgcolor='white',
            bordercolor='white'
        )
    ])
    fig2.update_xaxes(title='Hora do Dia')
    fig2.update_yaxes(title='Potência Ativa (pu)')
    fig2.update_layout(title='ANÁLISE SÁBADOS (SA)', grid=dict(columns=1, rows=1),
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      showlegend=True)

    # Salvando a figura em HTML
    pio.write_html(fig2, r'C:\pythonjr\aneel\UGMT_15732740\grafico_SA.html')
    print("Figura SÁBADOS salva em HTML com sucesso.")

    #################################################
    # Subplot para DOMINGOS
    for _, grupo in df_DO.groupby(df_DO['Data/Hora'].dt.date):
        fig3.add_trace(go.Scatter(x=grupo['Data/Hora'].dt.hour, y=grupo['kw'], mode='lines',
                                 name=grupo['Data/Hora'].iloc[0].strftime('%Y-%m-%d')))

    # Calcula a média para cada hora do dia em DIAS ÚTEIS
    media_DO = df_DO.groupby(df_DO['Data/Hora'].dt.hour)['kw'].mean()
    fig3.add_trace(go.Scatter(x=media_DO.index, y=media_DO, mode='lines', name='Média DOMINGOS',
                             line=dict(color='black', width=3)))

    # Adiciona o valor de max_kW_SAno gráfico
    fig3.update_layout(annotations=[
        dict(
            x=0.183,
            y=0.88,
            xref='paper',
            yref='paper',
            text=f'Máx kW (DO) = {max_kW_DO:.2f} kW\nUGMT = {mes_ugmt}',
            showarrow=False,
            bgcolor='white',
            bordercolor='white'
        )
    ])
    fig3.update_xaxes(title='Hora do Dia')
    fig3.update_yaxes(title='Potência Ativa (pu)')
    fig3.update_layout(title='ANÁLISE DOMINGOS (DO)', grid=dict(columns=1, rows=1),
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      showlegend=True)

    # Salvando a figura em HTML
    pio.write_html(fig3, r'C:\pythonjr\aneel\UGMT_15732740\grafico_DO.html')
    print("Figura DOMINGOS salva em HTML com sucesso.")

except FileNotFoundError:
    print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

