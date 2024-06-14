import pandas as pd
import os, re

# Defines which executable is malicious in logs marked as malicious
executable_pname_dict = {
    'ransomwarePOC': 'RansomwarePOC.',
    'ransim': 'powershell.exe',
    'ransim-slow': 'powershell.exe',
    'JavaRansomware': 'java.exe',
    'RAASNet-Crypto': 'payload_PyCryp',
    'RAASNet-AES': 'payload_PyAES.',
    'roar-AES-CTR': 'roar.exe',
    'roar-ChaCha20': 'roar.exe',
    'cry': 'cry.exe',
    'babuk': 'babuk.exe',
    'lockbit': 'lockbit.exe',
}

def read_file(file_path):
    """
    Read a log file and return a dataframe

    Returns:
        df(timestamp, pname, pid, tid, syscall, rcx, rdx, r8, r9)
    """
    df = pd.read_csv(file_path, header=None, names=["timestamp","pname", "pid", "tid", "syscall", "rcx", "rdx", "r8", "r9"])
    return df

def classify_malicious(df, file_name):
    """
        Classify which pname is malicious in a df

        Returns
            df(..., malicious)
    """
    malicious, executable = file_name.split('_')[:2]
    df['malicious'] = 0
    if malicious != 'benign':
        df.loc[df['pname'] == executable_pname_dict[executable], 'malicious'] = 1
        print(f'Classifying {file_name} as malicious, {sum(df["malicious"])} malicious entries found')

    return df


def read_all_logs(version, logs_dir = '../logs'):
    """
        Read all logs from logs directory up until version

        Returns
            df(timestamp, pname, pid, tid, syscall, rcx, rdx, r8, r9, malicious)
    """
    version_dirs = [ f.path for f in os.scandir(logs_dir) if f.is_dir() and bool(re.fullmatch(r'V\d+(-\d+)?', f.name)) ]

    files = []
    for version_dir in version_dirs:
        if int(os.path.basename(version_dir)[1]) > version:
            continue
        print(f'Reading logs from {version_dir}')
        version_files = os.listdir(version_dir)
        version_files = [os.path.join(version_dir, file) for file in version_files]
        files.extend(version_files)

    files = filter(lambda file: file.endswith('.log'), files)

    # Read all logs to df
    dfs = []
    for file in files:
        df = read_file(file)
        file_name = os.path.basename(file)
        df = classify_malicious(df, file_name)
        dfs.append(df)

    return pd.concat(dfs)

def read_log_file(file_path):
    """
    Read a log file and classify which pname is malicious

    Returns:
        df(timestamp, pname, pid, tid, syscall, rcx, rdx, r8, r9, malicious)
    """
    df = read_file(file_path)
    file_name = os.path.basename(file_path)
    df = classify_malicious(df, file_name)
    return df


def read_logs_from_dir(logs_dir):
    """
        Read all logs from logs directory

        Returns
            df(timestamp, pname, pid, tid, syscall, rcx, rdx, r8, r9, malicious)
    """
    files = os.listdir(logs_dir)
    files = [os.path.join(logs_dir, file) for file in files]

    files = filter(lambda file: file.endswith('.log'), files)

    # Read all logs to df
    dfs = []
    for file in files:
        df = read_log_file(file)
        dfs.append(df)

    return pd.concat(dfs)

if __name__ == '__main__':
    read_all_logs(1)