import socket
import os
from Controller.file_client import receive_file, extract_zip

# Constants
KEYWORD_NEXT_FILE = 'next_file'
KEYWORD_NEXT_LOG = 'next_log'

def create_socket(server_host, server_port):
    '''
    Create a socket and connect to the server
    '''
    return socket.create_connection((server_host, server_port))

def request_next_file(conn, target_dir):
    '''
    Request a file from the controller and save it to the target directory
    
    Parameters:
        conn (socket): The connection to the controller
        target_dir (str): The directory to save the file to
    '''
    conn.send(f'{KEYWORD_NEXT_FILE}'.encode())
    file_name = receive_file(conn, target_dir)
    return extract_zip(file_name)


def request_next_log(conn):
    '''
        Request the next log socket from the controller
    '''
    conn.send(f'{KEYWORD_NEXT_LOG}'.encode())
    settings_msg = conn.recv(1024).decode()
    malicious, filename, duration_minutes = settings_msg.split(';')
    return malicious, filename, int(duration_minutes)
