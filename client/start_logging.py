from HyperDbg import hyperdbg
from Controller import controller
import datetime
import os
import shutil
import time
from Controller.file_client import ReceiveFileException, NoFilesException
import subprocess
from System.recovery import recover
from System.efiguard import disable_dse
from System import runas
import threading
import subprocess

# constants
HYPERDBG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\\HyperDbg')
PSEXEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.\\System\\PsExec.exe')
CONTROLLER_IP = '192.168.8.3'
CONTROLLER_PORT = 9090
SAMPLE_DIR = 'C:\\Users\\Client\\Downloads'

def check_connection(conn):
    conn.sendall("test_connection".encode())
    conn.recv(1024).decode()

# disable DSE
print('Disabling DSE...')
disable_dse()
print('DSE disabled.')

# check if cred file exists
if not runas.cred_file_exists():
    runas.store_creds()


# check if hyperdbg is runnable
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_dir = f'running_{timestamp}.txt'
output_dir = os.path.join(os.getcwd(), output_dir)
test_ds_path = os.path.join(os.getcwd(), 'test.ds')
print('Checking if HyperDbg is runnable...')
hyperdbg.create_ds_file(hyperdbg.test_ds_template_path, hyperdbg.to_test_ds_template_dict(output_dir), test_ds_path)
runnable = hyperdbg.test_runnable(hyperdbg.bat_file_path, HYPERDBG_DIR, test_ds_path, output_dir)
os.remove(test_ds_path)
if not runnable:
    print('HyperDbg failed to start. Ensure that DSE is disabled')
    exit(1)

# check the connection to the controller
print('HyperDbg is runnable. Checking connection to controller...')
try:
    conn = controller.create_socket(CONTROLLER_IP, CONTROLLER_PORT)
    conn.settimeout(60)
    check_connection(conn)
except (ConnectionRefusedError, TimeoutError):
    print(f'Failed to connect to the controller. Ensure that the controller({CONTROLLER_IP}:{CONTROLLER_PORT}) is up and enabled.')
    exit(1)

print('Connection to controller successful.')

# start logging
print('Start logging...')

# request file from controller
try:
    while True:
        next_file = controller.request_next_file(conn, SAMPLE_DIR)
        print(f'Next file: {next_file}')
        malicious, filename, duration_minutes, requires_admin, recovery = controller.request_next_log(conn)
        logger_ds_path = os.path.join(os.getcwd(), 'logger.ds')
        hyperdbg.create_ds_file(hyperdbg.logger_ds_template_path, hyperdbg.to_logger_ds_template_dict(duration_minutes), logger_ds_path)
        hyperdbg.start_logging(HYPERDBG_DIR, logger_ds_path)
        time.sleep(10) # wait for HyperDbg to start
        if requires_admin:
            # launche execute.bat in next_file as admin
            print("Launching execute.bat as admin...")
            subprocess.run(f'{next_file}\\execute.bat', shell=True)
        else:
            # launche execute.bat in next_file as non-admin
            runas.runas_client(f'{next_file}\\execute.bat')
        # above command is asynchronous, so we wait defined duration_minutes and rely on execute.bat to finish whithin that time.
        time.sleep(duration_minutes * 60 + 10)
        if recovery is not None:
            thread = threading.Thread(target=recover, args=(recovery,))
            thread.start()
            while thread.is_alive():
                # keep connection alive
                check_connection(conn)
                time.sleep(30)
            thread.join()
        try:
            os.remove(logger_ds_path)
        except:
            print(f'Failed to remove {logger_ds_path}')
        try:
            shutil.rmtree(next_file)
        except:
            print(f'Failed to remove {next_file}')
except NoFilesException:
    print('No more files to log, finish process.')
except ReceiveFileException as e:
    print(f'Failed to receive file: {e}')
finally:
    conn.close()
    print('Connection to controller closed.')
    exit(0)



