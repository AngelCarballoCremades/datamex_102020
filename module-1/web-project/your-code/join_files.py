"""
Este archivo junta los archivos descargados en *monthly_download.py* y crea archivos *.cvs* por sistema, nodo y sistema.
Debes especificar el folder donde están tus archivos (con la estructura adecuada) en la función get_folder y modificar el folder de destino en el codigo principal.
"""

import pandas as pd
import os
import sys
import shutil

# Data and systems to join
datas = ['PND-MTR','PND-MDA','PML-MTR','PML-MDA']
systems = ['BCA','BCS','SIN']
markets = ['MTR','MDA']
node_types = ['PND','PML']

folder_frame = 'C:\\Users\\Angel\\Documents\\Ironhack\\web_project\\files'
def get_folder(data,system):
    """This function returns folder,files wher folder is the folder to look for files in the selected system and data, files is a list with the name of all the files available"""
    folder = f'{folder_frame}\\{data[:3]}\\{data[-3:]}'
    files_list = os.listdir(folder)
    files = [file for file in files_list if system in file] # Select files of indicated system by name

    return folder,files

def get_file_path(node_type, system, data):
    return f'{folder_frame}\\{system}-{node_type}-{data}.csv'

def join_small_csvs(folder, files, system, data):
    """This functions joins all csv files in 'files' list within 'folder' to the specified file"""
    out_filename = f'{folder_frame}\\{system}-{data}.csv'

    # values to add to file as columns: system and market
    market = data[-3:]
    string_byte = bytes(f'{system},{market},', 'ascii')
    header_byte = bytes(f'Sistema,Mercado,', 'ascii')

    with open(out_filename, 'wb') as outfile:
        for i, file in enumerate(files):

            with open(f'{folder}\\{file}', 'rb') as readfile:
                if i == 0:
                    for j in range(7):
                        readfile.readline()
                    line = readfile.readline()
                    outfile.write(header_byte+line)
                else:
                    readfile.readline()
                    readfile.readline()
                    readfile.readline()
                    readfile.readline()
                    readfile.readline()
                    readfile.readline()
                    readfile.readline()
                    readfile.readline()

                for line in readfile.readlines():
                    outfile.write(string_byte+line)

def join_big_csvs(node_type):
    """This functions joins all csv files in 'files' list within 'folder' to the specified file"""
    out_filename = f'{folder_frame}\\{node_type}.csv'

    print(node_type)

    with open(out_filename, 'wb') as outfile:

        for i,system in enumerate(systems):
            for j,market in enumerate(markets):

                file = f'{system}-{node_type}-{market}.csv'
                print(f'Joining {file}')

                with open(f'{folder_frame}\\{file}', 'rb') as readfile:

                    if i != 0 or j != 0:
                        readfile.readline()

                    shutil.copyfileobj(readfile, outfile, length=16*1024*1024)

                os.remove(f'{folder_frame}\\{file}')

    print(f'{node_type} Done.')


# Main code
for system in systems:

    for data in datas:

        folder,files = get_folder(data, system) # Get folder with files to be joined

        if len(files):

            print(f'{system}-{data} ', end = '')
            sys.stdout.flush() # Prints

            join_small_csvs(folder,files,system,data)

            print('Done')

        else:
            # If no files where found in folder the system-data is skipped
            print(f'\n{system}-{data} data not found.\n')

print('Finished joining files, merging by node type.')

for node_type in node_types:
    join_big_csvs(node_type)






print('----Finished----')



