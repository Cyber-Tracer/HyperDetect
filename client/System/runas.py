import os

SYS_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(SYS_DIR, 'cred.xml')
RUNAS_FILE = os.path.join(SYS_DIR, 'runas.ps1')
STORE_CREDS_FILE = os.path.join(SYS_DIR, 'store_credentials.ps1')

def cred_file_exists():
    return os.path.exists(CRED_FILE)

def store_creds():
    os.system(f'powershell -File {STORE_CREDS_FILE} {CRED_FILE}')

def runas_client(batch_file):
    os.system(f'powershell -File {RUNAS_FILE} {CRED_FILE} {batch_file}')