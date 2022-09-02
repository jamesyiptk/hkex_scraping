from selenium import webdriver
import traceback
import logging
import os
import sys
from datetime import datetime

input_date = sys.argv[1]
download_folder = sys.argv[2]
output_file = sys.argv[3]
logfile = sys.argv[4]

root_dict = os.path.split(os.path.realpath(sys.argv[0]))[0]
print(root_dict)

# define logfile
logfile_name = logfile

logging.basicConfig(filename=logfile_name, filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_folder}
options.add_experimental_option('prefs', prefs)
options.add_argument("--headless")
bro = webdriver.Chrome(executable_path=root_dict + r'\chromedriver.exe', options=options)
bro.maximize_window()
# hsi index constituents
root_urls = ["https://www.hsi.com.hk/static/uploads/contents/en/indexes/report/hsi/"]
for url in root_urls:
    date_obj = datetime.strptime(input_date, "%Y%m%d").date()
    filename = "HSI_" + date_obj.strftime("%d%b%y")+".xls"
    url = url+filename
    try:
        bro.get(url=url)
    except Exception as e:
        logging.error(e)
        traceback.print_exc(file=open(logfile_name, 'a+'))
        continue
# hsi notice
root_urls = ["https://www.hsi.com.hk/eng/newsroom/index-other-notices",
             "https://www.hsi.com.hk/chi/newsroom/index-other-notices",
             "https://www.hsi.com.hk/schi/newsroom/index-other-notices"]
File_Type = []
dateArray = []
FileName_Eng = []
FileName_TC = []
FileName_SC = []
URL_ENG = []
URL_TC = []
URL_SC = []
try:
    # Eng
    bro.get(url=root_urls[0])
    i = 0
    files_div = bro.find_elements_by_class_name("newsItem")
    for file_div in files_div:
        if i > 20:
            break
        date_title = file_div.find_elements_by_tag_name("div")
        File_Type.append("HSI")
        # dd = datetime.strptime(date_title[1].text, "%d %b %Y").date().strftime("%Y%m%d")
        # date format yyyymmdd
        dateArray.append(datetime.strptime(date_title[1].text, "%d %b %Y").date().strftime("%Y-%m-%d"))
        FileName_Eng.append(date_title[2].text)
        URL_ENG.append(date_title[3].find_element_by_tag_name("a").get_attribute("href"))
        i = i+1
    # TC
    i = 0
    bro.get(url=root_urls[1])
    files_div = bro.find_elements_by_class_name("newsItem")
    for file_div in files_div:
        if i > 20:
            break
        date_title = file_div.find_elements_by_tag_name("div")
        FileName_TC.append(date_title[2].text)
        URL_TC.append(date_title[3].find_element_by_tag_name("a").get_attribute("href"))
        i = i + 1

    # SC
    i = 0
    bro.get(url=root_urls[2])
    files_div = bro.find_elements_by_class_name("newsItem")
    for file_div in files_div:
        if i > 20:
            break
        date_title = file_div.find_elements_by_tag_name("div")
        FileName_SC.append(date_title[2].text)
        URL_SC.append(date_title[3].find_element_by_tag_name("a").get_attribute("href"))
        i = i + 1

    #  CSI 100 Notices
    root_urls = ["http://www.csindex.com.cn/zh-CN/search/total?about=000903",
                 "http://www.csindex.com.cn/en/search/total?about=000903"]
    # SC
    bro.get(url=root_urls[0])
    i = 0
    files_div = bro.find_element_by_class_name("newList")
    files_div = files_div.find_elements_by_tag_name("li")
    for file_div in files_div:
        if i > 4:
            break
        date = file_div.find_element_by_tag_name("span")
        File_Type.append("CSI100")
        name_link = file_div.find_element_by_tag_name("a")
        dateArray.append(date.text)
        FileName_SC.append(name_link.text)
        FileName_TC.append("")
        URL_SC.append(name_link.get_attribute("href"))
        URL_TC.append("")
        i = i+1
    # ENG
    i = 0
    bro.get(url=root_urls[1])
    files_div = bro.find_element_by_class_name("newList")
    files_div = files_div.find_elements_by_tag_name("li")
    for file_div in files_div:
        if i > 4:
            break
        name_link = file_div.find_element_by_tag_name("a")
        FileName_Eng.append(name_link.text)
        URL_ENG.append(name_link.get_attribute("href"))
        i = i + 1

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("File_Type|Date|FileName_Eng|FileName_TC|FileName_SC|URL_ENG|URL_TC|URL_SC\n")
    array_len = len(dateArray)
    for i in range(array_len):
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(
                File_Type[i] + "|" + dateArray[i] + "|" + FileName_Eng[i] + "|" + FileName_TC[i] + "|" + FileName_SC[i]
                + "|" + URL_ENG[i] + "|" + URL_TC[i] + "|" + URL_SC[i] + "\n")
    logging.info("Process finished")
except Exception as e:
    logging.error(e)
    traceback.print_exc(file=open(logfile_name, 'a+'))
    bro.quit()
bro.quit()
