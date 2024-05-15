import subprocess
import os
import zipfile

BACKUP_TARGET = 'D:'
FILE_BACKUP_PATH = 'D:\\FileBackup'
RECOVERY_PARENT_DIR = 'C:\\Users\\Client'

def get_version_information():
    """
    use wbadmin to get the version information of the backup

    Returns:
        str: Backup time
        str: Backup target
        str: Version identifier
        str: What backup can recover
        str: Snapshot ID
    
    """
    cmd_list = ['wbadmin', 'get', 'versions', f'-backupTarget:{BACKUP_TARGET}']
    result = subprocess.run(cmd_list, capture_output=True, text=True)
    
    # Check if the command was successful
    if result.returncode != 0:
        raise ValueError("Error listing backup versions")
    
    # Parse the output to find the first available backup version
    output_lines = result.stdout.split('\n')[3:8]
    output_lines = [line.split(': ')[1] for line in output_lines]
    
    return output_lines

def recover_files():
    """
    Recover files from FILE_BACKUP_PATH to DIRS_TO_RECOVER
    """
    zips = [f for f in os.listdir(FILE_BACKUP_PATH) if f.endswith('.zip')]
    for zip_file in zips:
        zip_path = os.path.join(FILE_BACKUP_PATH, zip_file)
        recovery_dir = os.path.join(RECOVERY_PARENT_DIR, os.path.splitext(zip_file)[0])
        if not os.path.exists(recovery_dir):
            print(f"{recovery_dir} not found, creating...")
            os.makedirs(recovery_dir)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all files
            zip_ref.extractall(recovery_dir)
            print(f"Files extracted to {recovery_dir}")


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
            backup_time, _, version_id, can_recover, _ = get_version_information()
            print("Not implemented yet")
        case _:
            raise ValueError("Invalid recovery mode")
        
if __name__ == '__main__':
    recover("client_files")
