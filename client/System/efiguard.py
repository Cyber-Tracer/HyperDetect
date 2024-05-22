import os

EFIGUARD_EXE_DIR = os.path.join(os.path.abspath(__file__), 'EfiDSEFix.exe')

def disable_dse():
    '''
    Disable DSE using EfiDSEFix.exe
    '''
    os.system(f'{EFIGUARD_EXE_DIR} -d')