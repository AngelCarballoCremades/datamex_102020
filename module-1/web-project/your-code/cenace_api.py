import os
import sys
import pdb
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date, timedelta
import json

datas = ['PND-MTR','PND-MDA']#,'PML-MTR','PML-MDA']
systems = ['BCA','BCS','SIN']
url_frame = f'https://ws01.cenace.gob.mx:8082/SWPEND/SIM/' # Agregar al final los parámetros un '/'

def file_path(data,system):

    file = f'C:\\Users\\Angel\\Documents\\Ironhack\\web_project\\files\\{system}-{data}.csv'
    return file

def get_json(nodes, dates, system, data):
    nodes_string = ''

    for node in nodes:
        nodes_string += f'{node},'

    nodes_string = nodes_string[:-1]

    url_complete = f'{url_frame}{system}/{data[-3:]}/{nodes_string}/{dates[0][:4]}/{dates[0][5:7]}/{dates[0][8:]}/{dates[1][:4]}/{dates[1][5:7]}/{dates[1][8:]}/JSON'

    req = requests.get(url_complete)
    soup = BeautifulSoup(req.content, 'html.parser')
    json_file = json.loads(str(soup.text))

    return json_file

def missing_dates(df,):
    today = date.today()
    last_date = df['Fecha'].max()

    year = int(last_date[:4])
    month = int(last_date[5:7])
    day = int(last_date[8:])
    last_date = date(year, month, day)
    begining_date = last_date + timedelta(days = 1)

    if data[-3:] == 'MDA':
        date_needed = today + timedelta(days = 1)

    elif data[-3:] == 'MTR':
        date_needed = today - timedelta(days = 7)

    days = (date_needed - last_date).days

    print(f'{system}-{data} Last date on record is {last_date}, there are {days} days missing until {date_needed}.')

    return days, begining_date

def get_nodes_api(nodes):

    nodes_api = []
    while True:
        if len(nodes) >= 10:
            nodes_api.append(nodes[:10])
            nodes = nodes[10:]
        else:
            nodes_api.append(nodes)
            break

    return nodes_api

def dates_intervals(days, begining_date):

    dates = []
    start_date = begining_date

    while days > 0:
        if days >= 7:
            end_date = start_date + timedelta(days = 6)
            dates.append( [str(start_date),str(end_date)] )
            start_date = end_date + timedelta(days = 1)
            days -= 7
        else:
            end_date = start_date + timedelta(days = days -1)
            dates.append( [str(start_date),str(end_date)] )
            # start_date = end_date + timedelta(days = 1)
            days = 0
    return dates

def get_data_frame(json_file):

    dfs = []
    for node in json_file['Resultados']:
        dfs.append(pd.DataFrame(node))

    df = pd.concat(dfs)

    df['Fecha'] = df['Valores'].apply(lambda x: x['fecha'])
    df['Hora'] = df['Valores'].apply(lambda x: x['hora'])
    df['Precio Zonal  ($/MWh)'] = df['Valores'].apply(lambda x: x['pz'])
    df['Componente energia  ($/MWh)'] = df['Valores'].apply(lambda x: x['pz_ene'])
    df['Componente perdidas  ($/MWh)'] = df['Valores'].apply(lambda x: x['pz_per'])
    df['Componente Congestion  ($/MWh)'] = df['Valores'].apply(lambda x: x['pz_cng'])
    df['Zona de Carga'] = df['zona_carga'].copy()
    df = df[['Fecha', 'Hora', 'Zona de Carga', 'Precio Zonal  ($/MWh)',
           'Componente energia  ($/MWh)', 'Componente perdidas  ($/MWh)',
           'Componente Congestion  ($/MWh)']]
    return(df)



system = systems[1]
data = datas[1]
for system in systems:
    for data in datas:

        df = pd.read_csv(file_path(data,system))

        nodes = [node.replace(' ', '-') for node in df['Zona de Carga'].unique().tolist()]
        # print(len(nodes))
        nodes_api = get_nodes_api(nodes)

        days,begining_date = missing_dates(df)

        dates = dates_intervals(days, begining_date)
        # print(dates)

        if len(dates):
            requests_left = len(nodes_api) * len(dates)
            dfs = []
            for node_group in nodes_api:
                for date_interval in dates:

                    print(f'{requests_left} requests left.')
                    json_file = get_json(node_group,date_interval,system,data)
                    dfs.append(get_data_frame(json_file))
                    requests_left -= 1

            df = pd.concat(dfs)
            df_prev = pd.read_csv(f'{file_path(data,system)}')

            df_final = pd.concat([df_prev,df])

            # print(df_final)

            df_final.sort_values(by = ['Zona de Carga','Fecha','Hora'], inplace = True ,ascending = [True,True,True])
            df_final.to_csv(f'{file_path(data,system)}', index = False)
            print(f'{system}-{data} up to date')

        else:
            print(f'{system}-{data} up to date')