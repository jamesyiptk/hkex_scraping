import logging
import sys
import pandas as pd
import hashlib
import requests


def get_html_md5(url):
    try:
        str_html = requests.get(str(url), timeout=2)
        html_hash = hashlib.md5(str_html.content)
        return html_hash.hexdigest()
    except requests.exceptions.ConnectTimeout:
        return "TimeOut"
    except Exception as e:
        logging.error(e)
        return "get_html_md5 Failed"


def get_file_md5(file):
    try:
        with open(file, 'rb') as f:
            content = f.read()
            file_hash = hashlib.md5(content)
            return file_hash.hexdigest()
    except Exception as e:
        logging.error(e)
        return "get_local_file_md5 Failed"


input_file = sys.argv[1]
output_file = sys.argv[2]
logfile = sys.argv[3]
# logfile_name = "\\\\S-HK-FILESRV\\DBEngines\\SmallEngines\\Tools\\python\\SETools\\Log\\SpiderHTMLSource_20190923.log"
logfile_name = logfile
logging.basicConfig(filename=logfile_name, filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


try:
    data = pd.DataFrame(pd.read_excel(input_file))
    un_match_count = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("CheckName,Url_Website,Hash_Website,Hash_Local,CheckResult\n")
    for row in data.itertuples():
        Hash_Website = get_html_md5(getattr(row, 'Path_Website'))
        if Hash_Website == "TimeOut":
            logging.info(getattr(row, 'Path_Website') + "Time Out")
        elif Hash_Website == "get_html_md5 Failed":
            logging.info(getattr(row, 'Path_Website') + "get_html_md5 Failed")
        Hash_Local = get_file_md5(getattr(row, 'Path_Local'))
        CheckName = getattr(row, 'CheckName')
        check_result = "Match\n" if Hash_Website == Hash_Local else "UnMatch\n"
        with open(output_file, 'a+', encoding='utf-8') as f:
            f.write(CheckName + "," + getattr(row, 'Path_Website') + "," + Hash_Website + "," + Hash_Local + "," + check_result)
    logging.info("Processed Finished")

except Exception as e:
    logging.error(e)
    print(e)
