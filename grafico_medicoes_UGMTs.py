import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings( 'ignore' )

## Escolha do medidor da usina a ser considerada na tabela geral de medições
medidor = 15732740

##Função Preparação EDP
def prep_medicao_edp(path_xlsx, medidor, ano):
    dff = pd.DataFrame()
    xls = pd.ExcelFile(path_xlsx)
    sheet_names = xls.sheet_names
    for sheet in sheet_names:
        df = pd.read_excel(path_xlsx, sheet_name=sheet, header=None)
        df.loc[1,0] = 'Data/Hora'
        df.columns = df.iloc[1].tolist()
        df = df[3:len(df)-1].reset_index(drop=True)
        df['Data/Hora'] = pd.to_datetime(df['Data/Hora'], format='%Y-%m/%d %H:%M:%S')
        df['Data'] = df['Data/Hora'].dt.date
        df['Hora'] = df['Data/Hora'].dt.time

        dff = pd.concat([dff, df],axis=0).reset_index(drop=True)
    dfid = dff[['Data/Hora','Data','Hora', medidor]]
    dfid.loc[:,'mes'] = dfid['Data/Hora'].dt.month
    dfid.loc[:,'ano'] = dfid['Data/Hora'].dt.year
    dfid = dfid[dfid['ano']==ano].reset_index(drop=True)
    return dfid

##Função set layout
def create_subplots(nrows, ncols, title):
    # Create subplots for each month arranged in a 3x4 grid
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=[f'Mês {i}' for i in range(1, 13)])

    for month in range(1, 13):
        df_month = dfid[dfid['mes'] == month]
        fig.add_trace(go.Scatter(x=df_month['Data/Hora'], y=df_month[medidor], mode='lines', name=f'Mês {month}', showlegend=False),
                      row=(month-1)//ncols + 1, col=(month-1)%ncols + 1)

    for clm in range(0, ncols):
        fig.update_xaxes(title_text="Data", row=nrows, col=clm+1)
    for rw in range(0, nrows):
        fig.update_yaxes(title_text="Potência (kW)", row=rw+1, col=1)


    fig.update_xaxes(gridcolor='lightgrey', griddash='dot',showgrid=True,showline=True, mirror=True,linewidth=1, linecolor='darkgrey')
    fig.update_yaxes(gridcolor='lightgrey', griddash='dot',showgrid=True,showline=True, mirror=True, linewidth=1, linecolor='darkgrey')
    fig.update_yaxes(range=[0, round(dfid[medidor].max())])

    fig.update_layout(title=title, template='plotly_white',font=dict(size=13, color='black'))

    fig.update_layout(title=dict(font = dict( color='black')), legend_title = dict(font = dict( color='black')),
                      legend = dict( font = dict(size=16,color='black')), font=dict(color='black'),
                      xaxis = dict( tickfont = dict(color='black')), yaxis = dict(tickfont = dict(color='black')),
                      xaxis_title= dict( font = dict(color='black')), yaxis_title= dict( font = dict(color='black')))
    return fig

#Path de Medições
path = r"C:\pythonjr\TED_ANEEL\medicoes12meses.xlsx"

#Criação
df = prep_medicao_edp(path, medidor, 2023)
dfid = df
print(df.shape)

# Preencher células vazias na quarta coluna com zeros
df.iloc[:, 3].fillna(0, inplace=True)
# Salvar DataFrame para Excel
df.to_excel(r"C:\pythonjr\TED_ANEEL\resultado.xlsx", index=False)

#Ajustes finos se necessário
nrows = 6
ncols = 2
title = ''
fig = create_subplots(nrows, ncols, title)
fig.show()

#Save
fig.write_html(r"C:\pythonjr\TED_ANEEL\resultado.html")
