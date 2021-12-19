from logging import getLogger
from snowflake.ingest import SimpleIngestManager
from snowflake.ingest import StagedFile
from snowflake.ingest.utils.uris import DEFAULT_SCHEME
from datetime import timedelta
from requests import HTTPError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PrivateFormat
from cryptography.hazmat.primitives.serialization import NoEncryption
import time
import datetime
import os

def get_private_key_passphrase():
  return 'Snowflake'
def create_ingester_manager(root,pipe):
    key_path=os.path.join(root,'key','rsa_key.p8')
    with open(key_path, 'rb') as pem_in:
        pemlines=pem_in.read()
        private_key_obj=load_pem_private_key(pemlines,get_private_key_passphrase().encode(),default_backend())
        private_key_text=private_key_obj.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode('utf-8')
        ingest_manager=SimpleIngestManager(account=os.getenv('SNOWFLAKE_ACCOUNT'),
                                        host=os.getenv('SNOWFLAKE_ACCOUNT')+"."+os.getenv('SNOWFLAKE_REGION')+'.snowflakecomputing.com',
                                        user=os.getenv('SNOWFLAKE_PIPE_USER'),
                                        pipe=pipe,
                                        private_key=private_key_text)
    return ingest_manager                                    
# List of files, but wrapped into a class
def ingest_files(File_List):
    file_list=File_List
    staged_file_list = []
    for file_name in file_list:
        staged_file_list.append(StagedFile(file_name, None))
    try:
        resp = ingest_manager.ingest_files(staged_file_list)
        print(resp)      
    except HTTPError as e:
        # HTTP error, may need to retry
        logger.error(e)  
        exit(1)
    assert(resp['responseCode'] == 'SUCCESS')    

def check_load_history(ingest_manager): 
    while True:
        history_resp = ingest_manager.get_history()
        if len(history_resp['files']) > 0:
            print('Ingest Report:\n')
            print(history_resp)
            break
        else:
            time.sleep(20)    
        minutes = timedelta(minutes=30)
        date = datetime.datetime.utcnow() - minutes
        history_range_resp = ingest_manager.get_history_range(date.isoformat() + 'Z')
        print('\nHistory scan report: \n')
        print(history_range_resp)