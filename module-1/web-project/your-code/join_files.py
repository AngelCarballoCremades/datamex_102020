"""
Este archivo junta los archivos descargados en *monthly_download.py* y crea archivos *.cvs* por sistema, nodo y sistema.
Debes especificar el folder donde están tus archivos (con la estructura adecuada) en la función get_folder y modificar el folder de destino en el codigo principal.
"""

import pandas as pd
import os
import sys

# Data and systems to join
datas = ['PND-MTR','PND-MDA','PML-MTR','PML-MDA']
systems = ['SIN','BCA','BCS']

def get_folder(data,system):
    """This function returns folder,files wher folder is the folder to look for files in the selected system and data, files is a list with the name of all the files available"""
    folder = f'C:\\Users\\Angel\\Documents\\Ironhack\\web_project\\files\\{data[:3]}\\{data[-3:]}'
    files_list = os.listdir(folder)
    files = [file for file in files_list if system in file] # Select files of indicated system by name

    return folder,files

def join_csvs(folder,files,system,data):
    """This functions joins all csv files in 'files' list within 'folder'. Returns a data frame of all csv files joined and sorted."""
    print(f'{system}-{data}')
    print('Joining files ', end = '')

    # Reads first file of the list
    df = pd.read_csv(f'{folder}\\{files[0]}', skiprows=7, usecols=[0,1,2,3,4,5,6])

    for i in range(1,len(files)):

        df_1 = pd.read_csv(f'{folder}\\{files[i]}', skiprows=7, usecols=[0,1,2,3,4,5,6]) # Read next file from list
        df = pd.concat([df,df_1]) # Join df_1 to main df

        print(f'{len(files)-i},', end = '')
        sys.stdout.flush() # Prints

    print('Done')
    df.sort_values(by = ['Zona de Carga','Fecha','Hora'], inplace = True ,ascending = [True,True,True]) #Sort df

    return df.reset_index(drop=True) # Return df


# Main code
for system in systems:

    for data in datas:

        folder,files = get_folder(data, system) # Get folder with files to be joined

        if len(files):

            df = join_csvs(folder,files,system,data) # Create a df with all files joined

            print('Creating .csv file...\n')
            df.to_csv(f'C:\\Users\\Angel\\Documents\\Ironhack\\web_project\\files\\{system}-{data}.csv', index = False) # Create csv file from joined csv's df

        else:
            # If no files where found in folder the system-data is skipped
            print(f'\n{system}-{data} data not found.\n')





