import os
import pdb
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# print([os.getcwd()])

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.dir", 'C:\\Users\\Angel\\Desktop')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")


driver = webdriver.Firefox(firefox_profile=profile)

driver.get('https://www.cenace.gob.mx/Paginas/SIM/Reportes/H_PreciosEnergiaSisMEM.aspx?N=5&opc=divCssPreEnergia&site=Precios%20de%20la%20energ%C3%ADa/Precios%20Marginales%20Locales/MDA/Diarios&tipoArch=C&tipoUni=SIN&tipo=Diarios&nombrenodop=Precios%20Marginales%20Locales')

driver.find_element_by_xpath('/html/body/form/div[4]/div[1]/div/div[1]/div[2]/div/table/tbody/tr/td[1]/div/ul/li[1]/div/span[3]').click()

xpaths = ['/html/body/form/div[4]/div[1]/div/div[1]/div[2]/div/table/tbody/tr/td[3]/div[1]/div/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[2]/a[1]/img',
'/html/body/form/div[4]/div[1]/div/div[1]/div[2]/div/table/tbody/tr/td[3]/div[1]/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]/a[1]/img',
'/html/body/form/div[4]/div[1]/div/div[1]/div[2]/div/table/tbody/tr/td[3]/div[1]/div/table/tbody/tr[4]/td[2]/table/tbody/tr[11]/td[2]/a[1]/img']

main_handle = driver.current_window_handle
print(main_handle)

file_selector = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpaths[0])))

file_selector.click()


WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

time.sleep(5)
wait = True
while wait:
    wait = False
    for file in os.listdir('C:\\Users\\Angel\\Desktop'):
        if ".part" in file:
            time.sleep(0.5)
            wait = True



windows_after = driver.window_handles
print(windows_after)
new_window = [x for x in windows_after if x != main_handle][0]
# driver.switch_to_window(new_window) <!---deprecated>
driver.switch_to.window(new_window)

file_selector = find_element_by_xpath(xpaths[1])

file_selector.click()





# for xpath in xpaths:
#     # pdb.set_trace()
#     file_selector = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))

#     file_selector.click()

#     driver.switchTo().window(main_handle)
#     # wait = True
#     # while wait:
#     #     wait = False
    #     for file in os.listdir('C:\\Users\\Angel\\Desktop'):
    #         if ".part" in file:
    #             time.sleep(0.5)
    #             wait = True



# driver.quit()