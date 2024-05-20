import subprocess
import os
import zipfile
import glob

BACKUP_TARGET = 'D:'
FILE_BACKUP_PATH = 'D:\\FileBackup'
RECOVERY_PARENT_DIR = 'C:\\Users\\Client'
SEVEN_ZIP_PATH = 'C:\\Program Files\\7-zip\\7z.exe'

def remove_files_in_dir(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)

def recover_files():
    """
    Recover files from FILE_BACKUP_PATH to DIRS_TO_RECOVER
    """
    zips = [f for f in os.listdir(FILE_BACKUP_PATH) if f.endswith('.7z')]
    for zip_file in zips:
        zip_path = os.path.join(FILE_BACKUP_PATH, zip_file)
        recovery_dir = os.path.join(RECOVERY_PARENT_DIR, os.path.splitext(zip_file)[0])
        print(f"Recovering {recovery_dir}...")
        if not os.path.exists(recovery_dir):
            print(f"{recovery_dir} not found, creating...")
            os.makedirs(recovery_dir)
        else:
            # Remove existing files
            remove_files_in_dir(recovery_dir)
        os.system(f'{SEVEN_ZIP_PATH} x {zip_path} -o{recovery_dir}')


def recover(mode):
    """
        Recover the system using the specified mode
        supported modes: 
            "client_files" - recover CLIENT_FILES_PATH directory, does not require restart
            "volume" - recover the entire volume, requires restart
    """

    match mode:
        case "client_files":
            print(f"Recovering files from {FILE_BACKUP_PATH}...")
            recover_files()
            print("File recovery complete.")
        case "volume":
            print("Not implemented yet")
        case _:
            raise ValueError("Invalid recovery mode")
        
if __name__ == '__main__':
    recover("client_files")
