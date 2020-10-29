import requests
from bs4 import BeautifulSoup
import os
from slugify import slugify
import time
import multiprocessing as mp

def index_page(link):

    try:
        req = requests.get(link)
        soup = BeautifulSoup(req.content, 'html.parser')
        file_name = f'{slugify(link)}.html'
        
        with open(file_name,'w', encoding='utf-8') as f:
            f.write(soup.prettify())

        print('.',end='')

    except:
        print(',',end='')
        pass

url = 'https://en.wikipedia.org/wiki/Data_science'
req = requests.get(url)

print(req.status_code)

soup = BeautifulSoup(req.content, 'html.parser')
elements = soup.find_all('a',{'href':True})
links = list(set([element['href'] for element in elements if element['href'][0] != '#']))

domain = 'http://wikipedia.org'

links_abs = [link for link in links if link[:4] == 'http' and '%' not in link]
links_rel = [f'{domain}{link}' for link in links if link[0] == '/' and '%' not in link]

links = list(set(links_abs + links_rel))

os.chdir(f'{os.getcwd()}\wikipedia')

start_time = time.time()

pool = mp.Pool(4)
res = pool.map(index_page,links[:10])
pool.close()
res

print("--- %s seconds ---" % (time.time() - start_time))
