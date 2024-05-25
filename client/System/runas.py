import os

SYS_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(SYS_DIR, 'cred.xml')
RUNAS_FILE = os.path.join(SYS_DIR, 'runas.ps1')

def runas_client(batch_file):
    os.system(f'powershell -File {RUNAS_FILE} -ArgumentList {batch_file},{CRED_FILE}')