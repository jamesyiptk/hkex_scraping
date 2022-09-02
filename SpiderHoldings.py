from selenium import webdriver
from bs4 import BeautifulSoup
import traceback
import logging
import os
import sys
import time
from datetime import datetime
from datetime import timedelta 	## modified by GB

from selenium.webdriver.common.action_chains import ActionChains

currentDate = datetime.now().strftime("%Y-%m-%d")
currentDate = datetime.strptime(currentDate, "%Y-%m-%d").date()
# 定义log文件及格式
stockcode = sys.argv[1]

querydate = sys.argv[2]

if querydate == 'yesterday':	
	querydate = (datetime.today()+timedelta(days=-1)).strftime("%Y-%m-%d")		## modified by GB

date = datetime.strptime(querydate, "%Y-%m-%d").date()		## modified by GB


query_year = querydate.split("-")[0]
query_month = querydate.split("-")[1]
query_day = querydate.split("-")[2]
#  print(stockcode)
#  stockcode = '07242'
rootdict = os.path.split(os.path.realpath(sys.argv[0]))[0]
print(rootdict)
# rootdict = r'H:\python\DownLoadFileOA'
writefiledict = sys.argv[3]
#writefiledict = 'C:\\temp\\'
logfile_name = sys.argv[4]
#  print(logfile_name)

logfile_name = "\\\\10.36.2.21\\DBEngines\\SmallEngines\\Tools\\python\\SETools\\Log\\SpiderHoldings.log"

logging.basicConfig(filename=logfile_name, filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if date >= currentDate:
    print("Datetime Error")
    logger.error("Datetime Error")
    quit()


options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0}
options.add_experimental_option('prefs', prefs)
#options.add_argument("--headless")
bro = webdriver.Chrome(executable_path=rootdict + r'\chromedriver.exe', options=options)
bro.maximize_window()
# open login page
bro.get(url="https://www.hkexnews.hk/sdw/search/searchsdw.aspx")

try:

    Date_Dom = bro.find_element_by_id('txtShareholdingDate')
    Date_Dom.click()

    YearDom = bro.find_element_by_xpath('//*[@id="date-picker"]/div[1]/b[1]')

    buttons = YearDom.find_elements_by_tag_name('button')
    for li in buttons:
        if li.get_attribute('data-value') == query_year:
            li.click()
            break

    MonthDom = bro.find_element_by_xpath('//*[@id="date-picker"]/div[1]/b[2]')

    buttons = MonthDom.find_elements_by_tag_name('button')
    for li in buttons:
        if li.get_attribute('data-value') == query_month:
            li.click()
            break

    DayDom = bro.find_element_by_xpath('//*[@id="date-picker"]/div[1]/b[3]')

    buttons = DayDom.find_elements_by_tag_name('button')
    for li in buttons:
        if li.get_attribute('data-value') == query_day:
            li.click()
            break

    ActionChains(bro).move_by_offset(500, 500).click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标

    stock_code_input = bro.find_element_by_id('txtStockCode')
    stock_code_input.send_keys(stockcode)
    time.sleep(5)
    btn = bro.find_element_by_id('btnSearch')
    btn.click()

    html = bro.page_source
    soup = BeautifulSoup(html, 'lxml')
	
    ShareHoldingDateDom = soup.find("input", {"id": "txtShareholdingDate"})
    ShareHoldingDate = ShareHoldingDateDom.get('value').replace("/", "-")
    if ShareHoldingDate != querydate:
        logging.warning("The result is error, not the querydate, please check")
        #  bro.quit()
        #  sys.exit()
    logger.info("Compare date successful: " + ShareHoldingDate)
    table = soup.findAll("table", {"class": "table table-scroll table-sort table-mobile-list"})
    #  print(table.tbody)
    filename = writefiledict + 'HKEX_ShareHolders_' + stockcode + '_' + str(querydate) + '.txt'	## modified by GB
    with open(filename, 'a', encoding='utf-8') as f:
        f.write('Shareholding Date: ' + querydate + '\r\nStock Code: ' + stockcode + ' \r\n')
    # sleep(20)
    for row in soup.findAll("table", {"class": "table table-scroll table-sort table-mobile-list"})[0].tbody.findAll('tr'):
        #  first_column = row.findAll('th')[0].contents
        for column in row.findAll('td'):
            if (column.findAll('div', {'class': 'mobile-list-heading'})[0].text != '% of the total number of Issued Shares/ Warrants/ Units:'):
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(column.findAll('div', {'class':'mobile-list-body'})[0].text + ' | ')
            else:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(column.findAll('div', {'class': 'mobile-list-body'})[0].text + '\r\n')
    bro.quit()
    logger.info("Execute successful")
except Exception as e:
    logging.error(e)
    traceback.print_exc(file=open(logfile_name, 'a+'))
    bro.quit()







