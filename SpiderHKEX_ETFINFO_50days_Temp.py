from selenium import webdriver
import selenium
from time import sleep
from bs4 import BeautifulSoup
import traceback
import logging
import sys
import os
import urllib.request
from pathlib import Path

# 定义log文件及格式
rootdict = os.path.split(os.path.realpath(sys.argv[0]))[0]
download_folder = sys.argv[2]
logfile = sys.argv[3]
print(rootdict)
#  logfile_name = "\\\\S-HK-FILESRV\\DBEngines\\SmallEngines\\Tools\\python\\SETools\\Log\\RunStaticPages_20190307.log"
logfile_name=logfile
logging.basicConfig(filename=logfile_name, filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
#  download_folder = 'C:\\temp\\'
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_folder, "download.prompt_for_download": False}
options.add_experimental_option('prefs', prefs)
options.add_argument("--headless")
bro = webdriver.Chrome(executable_path=rootdict + r'\chromedriver.exe', chrome_options=options)

# open login page
bro.get(url="https://www1.hkexnews.hk/search/titlesearch.xhtml")
try:

    stock_code_input = bro.find_element_by_id('searchStockCode')
    #  stock_code_input.send_keys("7242")
    jsstring = 'document.getElementById("searchStockCode").value="' + sys.argv[1] + '"'
    #  jsstring = 'document.getElementById("searchStockCode").value="07302"'
    bro.execute_script(jsstring)
    stock_code_input.click()
    sleep(5)
    #  get the first record in the list
    stockname = bro.find_element_by_xpath('//*[@id="autocomplete-list-0"]/div[1]/div[1]/table/tbody/tr[1]')
    stockname.click()
    # click apply btn
    btn = bro.find_element_by_class_name("filter__btn-applyFilters-js")
    btn.click()
    html = bro.page_source
    soup = BeautifulSoup(html, 'lxml')
    table_div = soup.findAll("div", {"class": "table-scroller"})
    sleep(5)
    i=1
    #  Download top 50 rows
    while(i<50):
        stringDocUrl ='//*[@id="titleSearchResultPanel"]/div/div[1]/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[4]/div[2]/a'

        doclink = bro.find_element_by_xpath(stringDocUrl)
        # doclink.click()
        doclinkstr = doclink.get_attribute('href')
        sleep(5)
        print(doclinkstr)
        #  jsdownload = 'document.getElementsByClassName("doc-link")[0].querySelector("a").click()'
        #  bro.execute_script(jsdownload)
        sleep(5)
        docname = str(doclinkstr.split(r'/')[-1])
        urllib.request.urlretrieve(doclinkstr, filename=download_folder + docname)
        #  docname.replace('ltn', '07302_')
        import os.path
        downloadfile = download_folder + docname.replace('.', "_"+sys.argv[1] + ".")
        if os.path.isfile(downloadfile):
            os.remove(downloadfile)
        #  sleep(3)
        os.rename(download_folder + docname, downloadfile)
        i=i+1
    bro.quit()
    logging.info("Execute successful")
except Exception as e:
    logging.error(e)
    print(e)
    traceback.print_exc(file=open(logfile_name, 'a+'))
    bro.quit()






