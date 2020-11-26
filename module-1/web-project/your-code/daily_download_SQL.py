"""
Analiza la última fecha presente en los .csv creados con monthly_download.py y utiliza la API del cenace (https://www.cenace.gob.mx/DocsMEM/2020-01-14%20Manual%20T%C3%A9cnico%20SW-PEND.pdf) para actualizar la información a la última fecha disponible, actualiza los archivos .csv .
Falta agregar la API de PML (https://www.cenace.gob.mx/DocsMEM/2020-01-14%20Manual%20T%C3%A9cnico%20SW-PML.pdf), no se ha realizado por el peso de los archivos (supera los 2 GB en .csv), se requieren modificaciones menores ya que el método de invocación es prácticamente el mismo.
"""

import os
import sys
import pdb
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date, timedelta
import json
import psycopg2 as pg2

# Data and system to be downloaded
datas = ['PND-MTR','PND-MDA']#,'PML-MTR','PML-MDA']
systems = ['BCA','BCS','SIN']
node_types = ['PND','PML']
markets = ['MDA','MTR']

# APIs url
url_frame = {}
url_frame['PND'] = f'https://ws01.cenace.gob.mx:8082/SWPEND/SIM/' # Agregar al final los parámetros un '/'
url_frame['PML'] = f'https://ws01.cenace.gob.mx:8082/SWPML/SIM/' # Agregar al final los parámetros un '/'


def get_unique_nodes(cursor, system, node_type, market = 'MTR'):

    if node_type == 'PML':
        cursor.execute("""SELECT clave_nodo FROM {}_{}_{} GROUP BY clave_nodo;""".format(system, node_type, market))
    elif node_type == 'PND':
        cursor.execute("""SELECT zona_de_carga FROM {}_{}_{} GROUP BY zona_de_carga;""".format(system, node_type, market))

    return cursor.fetchall()


def get_last_date(cursor, system, node_type, market):

    cursor.execute("""SELECT MAX(fecha) FROM {}_{}_{};""".format(system, node_type, market))
    return cursor.fetchall()[0][0]


def resquest_data(nodes, dates, system, node_type, market):

    # Building node string
    nodes_string = ','.join(nodes)

    # Select correct API base
    url = url_frame[node_type]

    # Building request url with data provided
    url_complete = f'{url}{system}/{market}/{nodes_string}/{dates[0][:4]}/{dates[0][5:7]}/{dates[0][8:]}/{dates[1][:4]}/{dates[1][5:7]}/{dates[1][8:]}/JSON'

    print('Requesting...', end='')
    sys.stdout.flush()

    req = requests.get(url_complete)

    if req.status_code != 200:
        print(req.status_code)
        print("Requesting again...", end='')
        sys.stdout.flush()

        req = requests.get(url_complete)
        if req.status_code != 200:
            print(req.status_code)
            sys.stdout.flush()
            raise

    print('Processing...', end='')
    sys.stdout.flush()

    soup = BeautifulSoup(req.content, 'html.parser')
    # print(soup.text)
    json_data = json.loads(str(soup.text))

    return json_data


def check_data(json_data, date_interval):
    if json_data['status'] == 'OK':

        first_date = json_data['Resultados'][0]['Valores'][0]['fecha']
        last_date = json_data['Resultados'][0]['Valores'][-1]['fecha']

        if [first_date,last_date] != date_interval:
            print('')
            print(f'Dates requested: {date_interval[0]} - {date_interval[1]}')
            print(f'Dates obtained: {first_date} - {last_date}')

    else:
        print()
        print(f"Data status not 'OK': {json_data['status']}")
        print(json_data)


def missing_dates(last_date, market):
    """Returns begining date to ask info for depending on df's last date detected and type of market, also returns days of info to be asked for"""
    today = date.today()

    begining_date = last_date + timedelta(days = 1) # Date to start asking for (last_date plus 1 day)

    # MDA is available from today +1
    if market == 'MDA':
        date_needed = today + timedelta(days = 1)

    # MTR is available from today -7
    elif market == 'MTR':
        date_needed = today - timedelta(days = 7)

    days = (date_needed - last_date).days # Total days needed to update

    print(f'{system}-{node_type}-{market} Last date on record is {last_date}, there are {days} days missing until {date_needed}.')
    return days, begining_date

def pack_nodes(raw_node_list, node_type):
    """Returns a list of lists with nodes, this is done because depending on node type we have a maximum number of nodes per request ()PND is 10 max and PML is 20 max. PML missing"""
    node_list = [node[0].replace(' ','-') for node in raw_node_list]

    size_limit = 10 if node_type == 'PND' else 20

    nodes_api = []
    while True:
        if len(node_list) >= size_limit:
            nodes_api.append(node_list[:size_limit])
            node_list = node_list[size_limit:]
        else:
            nodes_api.append(node_list)
            break

    return nodes_api

def pack_dates(days, begining_date):
    """Gets days to ask for info and start date, returns appropiate data intervals to assemble APIs url"""
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
            days = 0

    return dates


def json_to_dataframe(json_file):
    """Reads json file, creates a list of nodes DataFrames and concatenates them. After that it cleans/orders the final df and returns it"""
    dfs = []

    for node in json_file['Resultados']:
        dfs.append(pd.DataFrame(node))
        # print(node)

    df = pd.concat(dfs) # Join all data frames

    # Clean/order df to same format of existing csv files
    df['sistema'] = json_file['sistema']
    df['mercado'] = json_file['proceso']
    df['fecha'] = df['Valores'].apply(lambda x: x['fecha'])
    df['hora'] = df['Valores'].apply(lambda x: x['hora'])

    if json_file['nombre'] == 'PND':
        df['precio_e'] = df['Valores'].apply(lambda x: x['pz'])
        df['c_energia'] = df['Valores'].apply(lambda x: x['pz_ene'])
        df['c_perdidas'] = df['Valores'].apply(lambda x: x['pz_per'])
        df['c_congestion'] = df['Valores'].apply(lambda x: x['pz_cng'])
        df['zona_de_carga'] = df['zona_carga'].copy()
        df = df[['sistema','mercado','fecha','hora','zona_de_carga','precio_e','c_energia', 'c_perdidas','c_congestion']]

    if json_file['nombre'] == 'PML':
        df['precio_e'] = df['Valores'].apply(lambda x: x['pml'])
        df['c_energia'] = df['Valores'].apply(lambda x: x['pml_ene'])
        df['c_perdidas'] = df['Valores'].apply(lambda x: x['pml_per'])
        df['c_congestion'] = df['Valores'].apply(lambda x: x['pml_cng'])
        df['clave_nodo'] = df['clv_nodo'].copy()
        df = df[['sistema','mercado','fecha','hora','clave_nodo','precio_e','c_energia', 'c_perdidas','c_congestion']]

    return df



conn = pg2.connect(user='postgres', password='Licuadora1234', database='cenace')
cursor = conn.cursor()


for node_type in ['PML']:#node_types:
    for system in ['BCS']:#systems:

        # Node list to upload from sql database
        nodes = get_unique_nodes(cursor, system, node_type)

        # Prepare nodes for API requests
        nodes_packed = pack_nodes(nodes, node_type)

        for market in ['MDA']:#markets:


            last_date = get_last_date(cursor, system, node_type, market)
            days, begining_date = missing_dates(last_date, market)
            dates_packed = pack_dates(days, begining_date)
            # print(dates_packed)

            if len(dates_packed):

                total_requests = len(nodes_packed) * len(dates_packed)
                dfs = [] # List of missing info data frames

                i = 1
                for date_interval in dates_packed:
                    for node_group in nodes_packed:

                        print(f'{i}/{total_requests} ', end='')
                        sys.stdout.flush()

                        json_data = resquest_data(node_group, date_interval, system, node_type, market)
                        check_data(json_data, date_interval)

                        print('Appending...', end='')
                        sys.stdout.flush()

                        dfs.append(json_to_dataframe(json_data))
                        print('Done.')

                        i += 1

    #                     break
    #                 break
    #         break
    #     break
    # break

                df = pd.concat(dfs) # Join downloaded info in one data frame
                # print(dates_packed)
                # print(df)
             #    df_prev = pd.read_csv(f'{file_path(data,system)}') # Get existing info file

             #    df_final = pd.concat([df_prev,df]) # Join existing info with downloaded info

             #    # Order new data frame
             #    df_final.sort_values(by = ['Zona de Carga','Fecha','Hora'], inplace = True ,ascending = [True,True,True])

             #    # Overwrite existing file with updated file
             #    df_final.to_csv(f'{file_path(data,system)}', index = False)
             #    print(f'{system}-{data} up to date\n')

             # #If there are no updates to be made...
#             else:
#                 print(f'{system}-{data} up to date\n')

# print('.....................DONE.....................')

# conn.commit()
# conn.close()







# Main code
# for system in systems:
#     for data in datas:

#         df = pd.read_csv(file_path(data,system)) # Reads system and data existing file

#         nodes = [node.replace(' ', '-') for node in df['Zona de Carga'].unique().tolist()] # Unique list of nodes in system file

#         nodes_api = pack_nodes(nodes) # Prepares nodes for requests

#         days,begining_date = missing_dates(df) # Gets number of missing dates in info

#         dates = pack_dates(days, begining_date) # Prepares dates for requests

#         # If there are updates to be made...
#         if len(dates):
#             requests_left = len(nodes_api) * len(dates)
#             dfs = [] # List of missing info data frames

#             for node_group in nodes_api:

#                 for date_interval in dates:

#                     print(f'{requests_left} requests left.')
#                     json_file = get_json(node_group,date_interval,system,data) # Request and get json with data
#                     dfs.append(json_to_dataframe(json_file)) # Add new requested info to main data frame
#                     requests_left -= 1

#             df = pd.concat(dfs) # Join downloaded info in one data frame
#             df_prev = pd.read_csv(f'{file_path(data,system)}') # Get existing info file

#             df_final = pd.concat([df_prev,df]) # Join existing info with downloaded info

#             # Order new data frame
#             df_final.sort_values(by = ['Zona de Carga','Fecha','Hora'], inplace = True ,ascending = [True,True,True])

#             # Overwrite existing file with updated file
#             df_final.to_csv(f'{file_path(data,system)}', index = False)
#             print(f'{system}-{data} up to date\n')

#         #  If there are no updates to be made...
#         else:
#             print(f'{system}-{data} up to date\n')

# print('.....................DONE.....................')