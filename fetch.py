import csv
import sys
import json
import requests
import urllib.parse

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


print('Fetching CDC data is started!')

data_url_lists = [
#    'https://data.nhi.gov.tw/resource/Nhi_Fst/Fstdata.csv',
    'https://od.cdc.gov.tw/icb/%E6%8C%87%E5%AE%9A%E6%8E%A1%E6%AA%A2%E9%86%AB%E9%99%A2%E6%B8%85%E5%96%AE.csv',
    'https://od.cdc.gov.tw/icb/%E6%8C%87%E5%AE%9A%E6%8E%A1%E6%AA%A2%E9%86%AB%E9%99%A2%E6%B8%85%E5%96%AE(%E8%8B%B1%E6%96%87%E7%89%88).csv',
    'https://od.cdc.gov.tw/eic/covid19/covid19_free_rapid_antigen_test_clinics.csv',
    'https://od.cdc.gov.tw/eic/Day_Confirmation_Age_County_Gender_19CoV.csv',
    'https://od.cdc.gov.tw/eic/covid19/covid19_global_cases_and_deaths.csv',
    'https://od.cdc.gov.tw/eic/covid19/covid19_tw_specimen.csv',
    'https://od.cdc.gov.tw/emerging/the-list-of-communicable-disease-isolation-hospitals-and-responding-hospitals-2020-2022.csv',
]

data_url_encoding = [
    'utf-8',
    'big5-hkscs',
    'big5-hkscs',
    'utf-8',
    'utf-8',
    'utf-8',
    'utf-8',
    'utf-8',
]
data_url_index = 0

for data_url in data_url_lists:
    response = requests.get(data_url, verify=False)
    response.encoding = data_url_encoding[data_url_index]
    win_eof = '\r\n'
    unix_eof = '\n'
    resp_text = response.text
    if win_eof in response.text:
        resp_text = resp_text.split(win_eof)
    else:
        resp_text = resp_text.split(unix_eof)

    json_keys = list(csv.reader([resp_text[0]]))[0]
    contents = resp_text[1:-1]
    json_data = []
    json_name = data_url.split('/')[-1].replace('.csv', '')
    csv_file_name = urllib.parse.unquote(json_name) + '.csv'
    csv_contents = unix_eof.join(resp_text)
    file_handler = open(csv_file_name, 'w')
    file_handler.write(csv_contents)
    file_handler.close()

    json_file_name = urllib.parse.unquote(json_name) + '.json'
    file_handler = open(json_file_name, 'w')
    print('Processing the ' + json_file_name + ' has been started.')

    for content in contents:
        json_obj = {}
        index = 0
        line = list(csv.reader([content]))[0]
        for json_key in json_keys:
            json_obj[json_key] = line[index]
            index += 1
        json_data.append(json_obj)

    file_handler.write(json.dumps(json_data) + '\n')
    file_handler.close()
    data_url_index += 1

    print('Processing the ' + json_file_name + ' has been done.')

print('Fetching CDC data is done!')
