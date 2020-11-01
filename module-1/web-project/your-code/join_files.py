import pandas as pd
import sqlalchemy
import os

datas = ['PND-MTR','PND-MDA']#,'PML-MTR','PML-MDA']
systems = ['SIN','BCA','BCS']

def get_folder(data,system):

    folder = f'C:\\Users\\Angel\\Documents\\Ironhack\\web_project\\files\\{data[:3]}\\{data[-3:]}'
    files_list = os.listdir(folder)
    files = [file for file in files_list if system in file]
    return folder,files

def join_csvs(folder,files):

    df = pd.read_csv(f'{folder}\\{files[0]}', skiprows=7, usecols=[0,1,2,3,4,5,6])
    for i in range(1,len(files)):

        df_1 = pd.read_csv(f'{folder}\\{files[i]}', skiprows=7, usecols=[0,1,2,3,4,5,6])
        df_2 = pd.concat([df,df_1])
        df = df_2
        print(f'{i},', end = '')
    print('Done')
    # print(df)
    # print(df.columns)
    df.sort_values(by = ['Zona de Carga','Fecha','Hora'], inplace = True ,ascending = [True,True,True])

    return df.reset_index(drop=True)

for system in systems:
    for data in datas:
        folder,files = get_folder(data, system)
        print(folder,system)
        df = join_csvs(folder,files)


        df.to_csv(f'C:\\Users\\Angel\\Documents\\Ironhack\\web_project\\files\\{system}-{data}.csv', index = False)




