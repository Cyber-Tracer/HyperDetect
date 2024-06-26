"""
The main server script is responsible for managing the client connection. 
It listens for incoming connections and sends files to the client. 
It also manages the logging socket.
"""

import os
import socket
import argparse
from file_server import send_file
from log_server import create_log_socket, ClientCrashedException
import re
import json

# Constants
BUFFER_SIZE = 1024
SERVER_PORT = 9090
SERVER_IP = '0.0.0.0'
SETTINGS_FILE = 'settings.json'
SETTINGS_KEYS = ['file', 'malicious', 'minutes', 'name', 'requires_admin']

def to_log_file(log_dir, malicious, name, minutes):
    """
    Convert the input file name to a log file name
    expected name format: [malicious|benign]_[file_name]_[duration]min.zip
    """
    mal_str = 'malicious' if malicious else 'benign'
    return os.path.join(log_dir, f'{mal_str}_{name}_{minutes}min.log')

def send_log_settings(connection, malicious, filename, duration, requires_admin=False, recovery=None):
    """
    Send the log settings to the client

    Parameters:
        connection (socket): The connection socket
        malicious (bool): True if the file is malicious
        filename (str): The name of the file
        duration (int): The duration of each log in minutes
        requires_admin (bool): True if the executable requires admin rights
        recovery (str): The recovery method to use
    """
    settings = f"{malicious};{filename};{duration};{int(requires_admin)};{recovery}"
    connection.sendall(settings.encode())

def handle_client_crash(file_idx, file_settings, crashed_log_duration):
    """
        Handle a client crash by the method defined by on_crash in the settings
        Possible methods:
            - retry: Retry the last file (default)
            - skip: Skip the last file
            - retry_append: Retry the last file and append the logs collected for the remaining time
    """
    on_crash = file_settings[file_idx].get('on_crash', 'retry')
    match on_crash:
        case "retry":
            print("Retrying the last file...")
            return file_idx, file_settings
        case "skip":
            print("Skipping the last file...")
            return file_idx + 1, file_settings
        case "retry_append":
            print("Retrying the last file and appending remaining time...")
            file_settings[file_idx]['minutes'] = file_settings[file_idx]['minutes'] - crashed_log_duration
            file_settings[file_idx]['write_mode'] = 'a'
            return file_idx, file_settings



def handle_connection(connection, client_address, file_settings, log_dir):
    """
    Handle a connection with a client and provide an interface for client requests

    Parameters:
        connection (socket): The connection socket
        client_address (tuple): The address of the client
        file_settings (list): List of dictionaries with keys: file, malicious, minutes, name, requires_admin
        log_dir (str): The directory to save the logs to
    """
    print("Connection established with ", client_address)
    file_idx = 0
    log_file_name = None
    connection.settimeout(60)
    finished_logging = False
    try:
        while file_idx < len(file_settings):
            data = connection.recv(BUFFER_SIZE).decode()
            if not data:
                break
            match data:
                case "next_file":
                    send_file(connection, file_settings[file_idx]['file'])
                    print(f"Sent {os.path.basename(file_settings[file_idx]['file'])} to {client_address}")
                    log_file_name = to_log_file(log_dir, file_settings[file_idx]['malicious'], file_settings[file_idx]['name'], file_settings[file_idx]['minutes'])
                    finished_logging = False
                case "next_log":
                    if log_file_name is None:
                        print("No file was sent to client yet, cannot start logging...")
                        send_log_settings(connection, False, "NONE", 0)
                        continue
                    send_log_settings(connection, file_settings[file_idx]['malicious'], file_settings[file_idx]['name'], file_settings[file_idx]['minutes'], file_settings[file_idx]['requires_admin'], file_settings[file_idx].get('recovery', None))
                    create_log_socket(log_file_name, client_address[0], file_settings[file_idx].get('write_mode', 'w'))
                    finished_logging = True
                    file_idx += 1
                case "test_connection":
                    connection.sendall("ACK".encode())
                case _:
                    print("Unknown command: ", data)
    except (socket.timeout, ConnectionResetError):
        if not finished_logging:
            file_idx = file_idx -1 if file_idx > 0 else 0 # Retry the last file
        print("Client timed out, remaining files: ", len(file_settings) - file_idx)
    except ClientCrashedException as e:
        print(f"Client {client_address[0]} crashed after {e.minutes_logged} minutes while logging {log_file_name}, handling crash...")
        file_idx, file_settings = handle_client_crash(file_idx, file_settings, e.minutes_logged)
    connection.close()
    return file_idx

def create_server_socket(file_settings, log_dir):
    """
    Create a server socket and wait for incoming connections

    Parameters:
        settings (list): List of dictionaries with keys: file, malicious, minutes, name, requires_admin
        malicious (list): List of booleans indicating if the file is malicious
        log_dir (str): The directory to save the logs to
        duration (int): The duration of each log in minutes
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address, prevent "Address already in use" error
    sock.bind((SERVER_IP, SERVER_PORT))

    sock.listen(1)
    successful_logs = 0
    try:
        while successful_logs < len(file_settings):
            print(f'Waiting for connection, {successful_logs}/{len(file_settings)} logs completed...')
            connection, client_address = sock.accept()
            successful_logs += handle_connection(connection, client_address, file_settings[successful_logs:], log_dir)
    except KeyboardInterrupt:
        print('\nShutting down server...')
    finally:
        sock.close()


def get_settings(file_dir):
    """
    Read settings from settings.json, expected in input directory

    Output: List of dictionaries with keys: file, malicious, minutes, name, requires_admin
    """
    with open(os.path.join(file_dir, SETTINGS_FILE)) as f:
        settings = json.load(f)
    for i, setting in enumerate(settings):
        if not all(key in setting for key in SETTINGS_KEYS):
            raise ValueError(f"Invalid settings file {file_dir}/{SETTINGS_FILE}, missing keys in setting {i}")
        settings[i]['file'] = os.path.join(file_dir, setting['file'])
        if not os.path.exists(settings[i]['file']):
            raise ValueError(f"Invalid settings file {file_dir}/{SETTINGS_FILE}, file {settings[i]['file']} does not exist")
    return settings

def to_settings(file):
    """
    Convert the input file name to settings dictionary
    expected name format: [malicious|benign]_[file_name]_[duration]min.zip
    """
    matches = re.match(r"^(malicious|benign)_([\w-]+)_([\d]+)min\.zip$", os.path.basename(file))
    if not matches:
        return None
    malicious, name, minutes = matches.group(1) == 'malicious', matches.group(2), int(matches.group(3))
    requires_admin = input("Does the file require admin rights? (y/[n]): ").lower() == 'y'
    recovery = input("Enter the recovery method ([none => leave empty]/client_files/volume): ")
    if recovery not in [None, 'client_files', 'volume']:
        recovery = None
    print("Recovery method: ", recovery if recovery else "None")
    on_crash = input("Enter the on crash method ([retry]/skip/retry_append): ")
    if on_crash not in ['retry', 'skip', 'retry_append']:
        on_crash = 'retry'
    print("Crash method: ", on_crash if on_crash else "retry")
    return {'file': file, 'malicious': malicious, 'minutes': minutes, 'name': name, 'requires_admin': requires_admin, 'recovery': recovery, 'on_crash': on_crash}
    

# parse arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Main server, manages the client connection')
    parser.add_argument('--input', type=str, default=os.path.join(os.getcwd(),'test'),  help='zip-file or directory of zip files to send')
    parser.add_argument('--log_dir', type=str, default=os.getcwd(),  help='The directory to save the logs to')
    args = parser.parse_args()

    if not os.path.exists(args.log_dir) or not os.access(args.log_dir, os.W_OK) or not os.path.isdir(args.log_dir):
        print(f"log_dir {args.log_dir} does not exist or is not writable.")
        exit(1)

    if not os.path.exists(args.input) or not os.access(args.input, os.R_OK):
        print(f"Input {args.input} does not exist or is not readable.")
        exit(1)


    if os.path.isfile(args.input):
        file_dir = args.input
        settings = to_settings(file_dir)
        if not settings:
            print(f"Invalid input file {file_dir}, expected format: [malicious|benign]_[file_name]_[duration]min.zip")
            exit(1)
        
        create_server_socket([settings], args.log_dir)
    elif os.path.isdir(args.input):
        file_settings = get_settings(args.input)
        print("Send files in following order:")
        for i, setting in enumerate(file_settings):
            print(f"{i+1}.", os.path.basename(setting['file']))
        if not file_settings:
            print(f"No valid input files found in {args.input}")
            exit(1)
        create_server_socket(file_settings, args.log_dir)