import pandas as pd
import os

# Defines which executable is malicious in logs marked as malicious
executable_pname_dict = {
    'ransomwarePOC': 'RansomwarePOC.',
    'RanSim': 'Powershell.exe',
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
    return df


def read_all_logs(version, logs_dir = '../logs'):
    """
        Read all logs from logs directory up until version

        Returns
            df(timestamp, pname, pid, tid, syscall, rcx, rdx, r8, r9, malicious)
    """
    version_dirs = [ f.path for f in os.scandir(logs_dir) if f.is_dir() ]

    files = []
    for version_dir in version_dirs[:version]:
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
        df = read_file(file)
        file_name = os.path.basename(file)
        df = classify_malicious(df, file_name)
        dfs.append(df)

    return pd.concat(dfs)

if __name__ == '__main__':
    read_all_logs(1)