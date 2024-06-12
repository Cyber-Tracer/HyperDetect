import subprocess
import os
import time

dir_path = os.path.dirname(os.path.abspath(__file__))
bat_file_path = os.path.join(dir_path, 'startHyperDbg.bat')
test_ds_template_path = os.path.join(dir_path, 'ds_templates/test_template.ds')
logger_ds_template_path = os.path.join(dir_path, 'ds_templates/logger_template.ds')


def start(bat_file_path, hyperdbg_dir, ds_path):
    cmd = ["powershell", "Start-process", "cmd", "-Args", f"/c\"{bat_file_path} {hyperdbg_dir} {ds_path}\"", "-Verb", "RunAs"]
    subprocess.run(cmd, check=True)

def wait_for_file(filename, timeout=60):
    start_time = time.time()
    while True:
        if os.path.exists(filename):
            time.sleep(5) # Wait for the file to be written by HyperDbg
            return True
        elif time.time() - start_time > timeout:
            return False
        else:
            time.sleep(1)

def to_test_ds_template_dict(output_file):
    return {'$$_output_file_$$': output_file}

def to_ms_hex(duration_minutes):
    milliseconds = duration_minutes * 60 * 1000
    # Convert the milliseconds to hexadecimal without the '0x' prefix
    return hex(milliseconds)[2:]

def to_logger_ds_template_dict(duration_minutes):
    return {'$$_duration_ms_hex_$$': str(to_ms_hex(duration_minutes))}

def create_ds_file(ds_template_path, arg_dict, output_path):
    with open(ds_template_path, 'r') as f:
        ds_template = f.read()
    for key, value in arg_dict.items():
        ds_template = ds_template.replace(key, value)
    with open(output_path, 'w') as f:
        f.write(ds_template)

def test_runnable(bat_file_path, hyperdbg_dir, ds_path, output_dir):
    '''
    Check if HyperDbg is runnable on the system by starting it and checking if it writes 'Running' to a file.

    Parameters:
        bat_file_path (str): Path to the batch file that starts HyperDbg.
        hyperdbg_dir (str): Path to the HyperDbg directory.
        ds_path (str): Path to the hyperdbg script file.
        output_dir (str): Path to the file that HyperDbg writes to.
    '''
    runnable = False
    try:
        start(bat_file_path, hyperdbg_dir, ds_path)
        if wait_for_file(output_dir):
            with open(output_dir, 'r') as f:
                if f.read() == 'Running':
                    runnable = True
            os.remove(output_dir)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start HyperDbg: {e}")
    
    return runnable

def start_logging(hyperdbg_dir, logger_ds_path):
    start(bat_file_path, hyperdbg_dir, logger_ds_path)
    

if __name__ == '__main__':
    output_dir = './running.txt'
    hyperdbg_dir = 'C:\\HyperDtct\\HyperDbg'
    ds_path = os.path.join(os.getcwd(), 'test.ds')
    create_ds_file(test_ds_template_path, to_test_ds_template_dict(output_dir), ds_path)
    runnable = test_runnable(bat_file_path, hyperdbg_dir, ds_path, output_dir)
    os.remove('test.ds')
    print("HyperDbg is runnable" if runnable else "HyperDbg failed to start")