import os
import glob
import datetime
from pcloud import PyCloud


pcloud_user = os.getenv('pcloud_user')
pcloud_password = os.getenv('pcloud_password')

files = []
files.extend(glob.glob('./*.json'))
files.extend(glob.glob('./*.csv'))

pc = PyCloud(pcloud_user, pcloud_password, endpoint='nearest')
response = pc.uploadfile(files=files, path='/cdc-data-mirror')

if type(response) is dict and response['result'] == 0:
    now_datetime = str(datetime.datetime.utcnow())
    log_handler = open('./pcloud_upload.log', 'w')
    log_handler.write('Last uploading time: ' + now_datetime)
    log_handler.close()
    print('Sync CSV and JSON files are successful!')
