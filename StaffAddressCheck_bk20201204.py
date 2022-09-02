import tabula
import requests
import sys
import logging
import pandas as pd
import csv
import traceback
import pdfplumber

download_file_path = sys.argv[1]
input_address_path = sys.argv[2]
output_file_path = sys.argv[3]
logfile_name = sys.argv[4]


#  gov_infect_address_dataframe = pd.read_csv(r'H:\python\DownLoadFileOA\building_list_chi_20200916.csv')
try:
    '''
    download_file_path = r'H:\python\DownLoadFileOA\building_list_chi_20200916.pdf'
    download_file_2_csv_path = r'H:\python\DownLoadFileOA\building_list_chi_20200916.csv'
    input_address_path = r'H:\python\DownLoadFileOA\Staff_Address.xlsx'
    output_file_path = r'H:\python\DownLoadFileOA\OutPut_file.xlsx'
    logfile_name = r'H:\python\DownLoadFileOA\infected_address_log_20200916.log'
    '''
    logging.basicConfig(filename=logfile_name, filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    url = "https://www.chp.gov.hk/files/pdf/building_list_chi.pdf"
    r = requests.get(url, allow_redirects=True)
    open(download_file_path, 'wb').write(r.content)
    #  tabula.convert_into(download_file_path, download_file_2_csv_path, output_format="csv", pages='all')
    inhouse_address_dataframe = pd.read_excel(input_address_path, header=0)

    pdf = pdfplumber.open(download_file_path)
    table_list = []
    for page in pdf.pages:
        # page0 = pdf.pages[0]

        table_page = page.extract_table()
        table_list.append(table_page)


    #  gov_infect_address_dataframe = pd.read_csv(download_file_2_csv_path)
    with open(output_file_path, 'a') as output_file:
        output_file.write("Name;Result;Address\n")

    data_structure = pd.DataFrame(columns=('Name', 'Result', 'Address'))

    intindex=0
    for index, row in inhouse_address_dataframe.iterrows():

        staff_address = str(row["住址"])
        staff_name = row["姓名"]
        logging.info("Begin to process" + staff_name)
        if staff_address == "nan":
            continue
        for table in table_list:
            for row in table:
                intindex = intindex + 1
                if str(row[1]).find(staff_address) == -1:
                    continue
                else:
                    data_structure.loc[intindex] = {'Name': staff_name,
                                                    'Result': 'Matched',
                                                    'Address': staff_address
                                                    }

    data_structure.to_excel(output_file_path, sheet_name='Result', index=False)
    logging.info("Executed successfully")
except Exception as e:
	logging.error("Error:")
	traceback.print_exc(file=open(logfile_name,'a+'))
