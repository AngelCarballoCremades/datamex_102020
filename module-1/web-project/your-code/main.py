# import os
# import pdb
# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # print([os.getcwd()])
# download_folder = 'C:\\Users\\Angel\\Desktop\\files'
# main_url = 'https://www.cenace.gob.mx/Paginas/SIM/Reportes/H_PreciosEnergiaSisMEM.aspx?N=5&opc=divCssPreEnergia&site=Precios%20de%20la%20energ%C3%ADa/Precios%20Marginales%20Locales/MDA/Diarios&tipoArch=C&tipoUni=SIN&tipo=Mensuales&nombrenodop=Precios%20Marginales%20Locales'
# xpath_timelapse = '/html/body/form/div[4]/div[1]/div/div[1]/div[2]/div/table/tbody/tr/td[1]/div/ul/li[2]/div/span[3]'
# element_dict = {'file':'/td[2]/a[1]/img', 'month':'/td[1]','date':'/td[3]'}
# xpath_files = '/html/body/form/div[4]/div[1]/div/div[1]/div[2]/div/table/tbody/tr/td[3]/div[1]/div/table/tbody/tr[{table_2en2}]/td[2]/table/tbody/tr[{month_period_12}]{element_dict[]}'


# def open_driver():

#     profile = webdriver.FirefoxProfile()
#     profile.set_preference("browser.download.folderList", 2)
#     profile.set_preference("browser.download.dir", download_folder)
#     profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
#     print('Opening Browser.')
#     driver = webdriver.Firefox(firefox_profile=profile)


# # driver.get('https://www.cenace.gob.mx/Paginas/SIM/Reportes/H_PreciosEnergiaSisMEM.aspx?N=5&opc=divCssPreEnergia&site=Precios%20de%20la%20energ%C3%ADa/Precios%20Marginales%20Locales/MDA/Diarios&tipoArch=C&tipoUni=SIN&tipo=Diarios&nombrenodop=Precios%20Marginales%20Locales')

# def get_url(url):
#     driver.get(url)

# def find_and_click(element_xpath,*i = 0):
#     if i == 0:
#         driver.WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, element_xpath))).click()
#     else:
#         driver.WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, element_xpath.format(i[0],i[1])))).click()


# def wait_download(directorio,i):

#     while directorio == os.listdir(download_folder):
#         pass

#     time.sleep(1)
#     print(f'Descargando {i}', end = '')

#     wait = True
#     while wait:
#         wait = False
#         for file in os.listdir(download_folder):
#             if ".part" in file:
#                 time.sleep(0.5)
#                 wait = True
#                 print('.', end = '')
#     print('Listo')



# open_driver()
# get_url(main_url)
# find_and_click(xpath_timelapse)

# print('Inicio')
# for table in range(2,73,2):
#     xpath = xpath_files.format()

#     find_and_click()
#     directorio = os.listdir(download_folder)

#     file_selector.click()

#     wait_download(directorio,i)

# print(f'Listos {i}')

# driver.quit()



import os
import pdb
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# print([os.getcwd()])
download_folder = 'C:\\Users\\Angel\\Desktop\\files'
main_url = 'https://www.cenace.gob.mx/Paginas/SIM/Reportes/H_PreciosEnergiaSisMEM.aspx?N=5&opc=divCssPreEnergia&site=Precios%20de%20la%20energ%C3%ADa/Precios%20Marginales%20Locales/MDA/Diarios&tipoArch=C&tipoUni=SIN&tipo=Mensuales&nombrenodop=Precios%20Marginales%20Locales'
xpath_timelapse = '/html/body/form/div[4]/div[1]/div/div[1]/div[2]/div/table/tbody/tr/td[1]/div/ul/li[2]/div/span[3]'
element_dict = {'file':'/td[2]/a[1]/img', 'month':'/td[1]','date':'/td[3]'}
xpath_frame = '/html/body/form/div[4]/div[1]/div/div[1]/div[2]/div/table/tbody/tr/td[3]/div[1]/div/table/tbody/tr[{t}]/td[2]/table/tbody/tr[{r}]{type}'

def wait_download(directorio,month,date):

    while directorio == os.listdir(download_folder):
        pass

    time.sleep(1)
    print(f'{month} {date}', end = '')

    wait = True
    while wait:
        wait = False
        for file in os.listdir(download_folder):
            if ".part" in file:
                time.sleep(0.5)
                wait = True
                print('.', end = '')
    print('Listo')

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.dir", download_folder)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
print('Opening Browser.')
driver = webdriver.Firefox(firefox_profile=profile)

print('Loading page.')
driver.get(main_url)

print('Selecting timelapse')
driver.find_element_by_xpath(xpath_timelapse).click()

print('...')

for table in range(2,73,2):
    for row in range(1,3):

        xpath_file = xpath_frame.format(t=table, r=row, type=element_dict['file'])
        xpath_month = xpath_frame.format(t=table, r=row, type=element_dict['month'])
        xpath_date = xpath_frame.format(t=table, r=row, type=element_dict['date'])

        file_button = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, xpath_file)))
        file_month = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, xpath_month))).text
        file_date = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, xpath_date))).text

        directorio = os.listdir(download_folder)

        file_button.click()

        wait_download(directorio,file_month,file_date)

print(f'Listos {table}')

driver.quit()

