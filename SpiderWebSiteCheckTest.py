import logging
import sys
import pandas as pd
import hashlib
import requests


def get_html_md5(url):
    for i in range(3):
        try:
            str_html = requests.get(str(url), timeout=2)
            html_hash = hashlib.md5(str_html.content)
            return html_hash.hexdigest()
        except requests.exceptions.ConnectTimeout as e:
            logging.error(e)
        except Exception as e:
            logging.error(e)
    return "get_html_md5 Failed"


input_file = r'\\10.36.2.21\DBEngines\SmallEngines\WWW-Daily\include\WebsitePages_CheckMd5_filelist_test.xlsx'
logfile = r'\\10.36.2.21\DBEngines\SmallEngines\Tools\python\SETools\Log\SpiderHTMLSource_20210514.log'
# logfile_name = "\\\\S-HK-FILESRV\\DBEngines\\SmallEngines\\Tools\\python\\SETools\\Log\\SpiderHTMLSource_20190923.log"
logfile_name = logfile
logging.basicConfig(filename=logfile_name, filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


try:
    while True:
        data = pd.DataFrame(pd.read_excel(input_file))
        for row in data.itertuples():
            Hash_Website = get_html_md5(getattr(row, 'Path_Website'))
            if Hash_Website == "TimeOut":
                logging.info(getattr(row, 'Path_Website') + "Time Out")
            elif Hash_Website == "get_html_md5 Failed":
                logging.info(getattr(row, 'Path_Website') + "get_html_md5 Failed")
        logging.info("Processed Finished")
except Exception as e:
    logging.error(e)
    print(e)
