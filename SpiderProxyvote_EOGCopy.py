from selenium import webdriver
import traceback
import logging
import sys
import os
from time import sleep

import re
from datetime import datetime

# 定义log文件及格式

root_dict = os.path.split(os.path.realpath(sys.argv[0]))[0]
last_date = sys.argv[1]
download_folder = sys.argv[2] + "\\"
log_file = sys.argv[3]
'''
root_dict = "\\\\S-HK-FILESRV\\DBEngines\\SmallEngines\\Tools\\python\\SETools\\Spiderman\\"
last_date = "2021-03-03"
download_folder = "\\\\S-HK-FILESRV\\DBEngines\\SmallEngines\\DataSources\\OtherParties\\other\\"
log_file = "\\\\S-HK-FILESRV\DBEngines\\SmallEngines\\Tools\\python\\SETools\\Log\\Spiderman_202100305.log"
'''
# logfile_name = "\\\\S-HK-FILESRV\\DBEngines\\SmallEngines\\Tools\\python\\SETools\\Log\\RunStaticPages_20190307.log"
logging.basicConfig(filename=log_file, filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# download_folder = '\\\\S-HK-FILESRV\\DBEngines\\SmallEngines\\Tools\\python\\SETools\\Log\\'
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_folder, "download.prompt_for_download": False}
options.add_experimental_option('prefs', prefs)
options.add_argument("--headless")
bro = webdriver.Chrome(executable_path=root_dict + r'\chromedriver.exe', options=options)
bro.maximize_window()
# open login page
bro.get(url="https://east.proxyedge.com/PEWeb/")
try:
    # login
    input_email = bro.find_element_by_xpath('/html/body/div/div[1]/div/form/input[8]')
    input_email.send_keys('conver.zou@efunds.com.hk')
    input_password = bro.find_element_by_xpath('/html/body/div/div[1]/div/form/input[9]')
    input_password.send_keys('HKabc123#')

    login_button = bro.find_element_by_xpath('/html/body/div/div[1]/div/form/button')
    login_button.click()
    # open data extract
    # Report = bro.find_element_by_xpath('/html/body/div/div/nav/div/div[2]/ul[1]/li[4]/a').click()
    jsstring = 'document.getElementsByTagName("li")[21].childNodes[0].click()'
    bro.execute_script(jsstring)
    sleep(10)
    '''
    Data_Extract = bro.find_element_by_xpath('/html/body/div/div/nav/div/div[2]/ul[1]/li[4]/ul/li[3]/a').click()
    sleep(5)
    '''
    Completed_Extract = bro.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[1]/div[1]/span[2]').click()
    sleep(5)
    Result_Table = bro.find_element_by_xpath("/html/body/div[1]/div/div[5]/div[4]/form/div[2]/div[3]/table")
    sleep(2)
    Tr_Lines = Result_Table.find_elements_by_tag_name("tr")
    for Tr_Line in Tr_Lines:
        datetime_string = Tr_Line.get_attribute('innerHTML')
        mat = re.search(r"(\d{2}-\w{3}-\d{4}\s\d{2}:\d{2}:\d{2}\s\w{2})", datetime_string)
        if mat is None:
            continue
        elif len(mat.groups()) > 0:
            dob_python = datetime.strptime(mat.groups()[0], '%d-%b-%Y %I:%M:%S %p').date()
        delta = dob_python - datetime.strptime(last_date, '%Y-%m-%d').date()
        print(delta.days)
        if delta.days <= 0:
            break
        Td_Cells = Tr_Line.find_elements_by_tag_name("td")
        for Td_Cell in Td_Cells:
            if Td_Cell.text.find("Proxyvote_EOG72")!=-1:
                Td_Cell.click()
                sleep(10)
                break
    bro.quit()
    logging.info("Execute successful")
except Exception as e:
    logging.error(e)
    print(e)
    traceback.print_exc(file=open(log_file, 'a+'))
    bro.quit()






