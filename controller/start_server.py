"""
The main server script is responsible for managing the client connection. 
It listens for incoming connections and sends files to the client. 
It also manages the logging socket.
"""

import os
import socket
import argparse
from file_server import send_file, send_no_files
from log_server import create_log_socket
import re

# Constants
BUFFER_SIZE = 1024
SERVER_PORT = 9090
SERVER_IP = '0.0.0.0'

def to_log_file(input_file, log_dir):
    """
    Convert the input file name to a log file name
    expected name format: [malicious|benign]_[file_name]_[duration]min.zip
    """
    file_name = os.path.basename(input_file)
    file_name = os.path.splitext(file_name)[0]
    return os.path.join(log_dir, file_name + '.log')

def send_log_settings(connection, malicious, filename, duration):
    """
    Send the log settings to the client

    Parameters:
        connection (socket): The connection socket
        malicious (bool): True if the file is malicious
        filename (str): The name of the file
        duration (int): The duration of each log in minutes
    """
    settings = f"{malicious};{filename};{duration}"
    connection.sendall(settings.encode())

def get_log_settings(log_file_name):
    """
    Get the log settings from the log file name

    Parameters:
        log_file_name (str): The name of the log file

    Returns:
        tuple: A tuple containing the malicious flag, the file name and the duration as int
    """
    file_name = os.path.splitext(os.path.basename(log_file_name))[0]
    parts = file_name.split('_')
    return parts[0] == 'malicious', parts[1], int(parts[2].replace('min', ''))


def handle_connection(connection, client_address, files_to_send, log_dir):
    """
    Handle a connection with a client and provide an interface for client requests

    Parameters:
        connection (socket): The connection socket
        client_address (tuple): The address of the client
        files_to_send (list): List of file paths to send to the client
        malicious (list): List of booleans indicating if the file is malicious
        log_dir (str): The directory to save the logs to
        duration (int): The duration of each log in minutes
    """
    print("Connection established with ", client_address)
    file_idx = 0
    log_file_name = None
    while True:
        data = connection.recv(BUFFER_SIZE).decode()
        if not data:
            break
        match data:
            case "next_file":
                if file_idx >= len(files_to_send):
                    send_no_files(connection)
                    continue
                send_file(connection, files_to_send[file_idx])
                print(f"Sent {os.path.basename(files_to_send[file_idx])} to {client_address}")
                log_file_name = to_log_file(files_to_send[file_idx], log_dir)
                file_idx += 1
            case "next_log":
                if log_file_name is None:
                    print("No file was sent to client yet, cannot start logging...")
                    send_log_settings(connection, False, "NONE", 0)
                    continue
                malicious, filename, duration = get_log_settings(log_file_name)
                send_log_settings(connection, malicious, filename, duration)
                create_log_socket(log_file_name, client_address[0])
            case "test_connection":
                connection.sendall("ACK".encode())
            case _:
                print("Unknown command, closing connection to ", client_address)
                break
    connection.close()

def create_server_socket(files_to_send, log_dir):
    """
    Create a server socket and wait for incoming connections

    Parameters:
        files_to_send (list): List of file paths to send to the client
        malicious (list): List of booleans indicating if the file is malicious
        log_dir (str): The directory to save the logs to
        duration (int): The duration of each log in minutes
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))

    sock.listen(1)
    try:
        while True:
            print('Waiting for new connection...')
            connection, client_address = sock.accept()
            handle_connection(connection, client_address, files_to_send, log_dir)
    except KeyboardInterrupt:
        print('\nShutting down server...')
    finally:
        sock.close()

def verify_input_file(file_dir):
    """
    Verify the input file name
    expected name format: [malicious|benign]_[file_name]_[duration]min.zip
    """
    file_name = os.path.basename(file_dir)
    return bool(re.match(r"^(malicious|benign)_[\w-]+_[\d]+min\.zip$", file_name))


# parse arguments
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
    if not verify_input_file(file_dir):
        print(f"Input file {file_dir} does not match expected format [malicious|benign]_[file_name]_[duration]min.zip")
        exit(1)
    create_server_socket([file_dir], args.log_dir)
elif os.path.isdir(args.input):
    files_to_send = [os.path.join(args.input, f) for f in os.listdir(args.input) if verify_input_file(f)]
    files_to_send = sorted(files_to_send, key=lambda name: ('malicious' in name, name))
    print("Send files in following order:")
    for i, file in enumerate(files_to_send):
        print(f"{i+1}.", os.path.basename(file))
    if not files_to_send:
        print(f"No valid input files found in {args.input}")
        exit(1)
    create_server_socket(files_to_send, args.log_dir)