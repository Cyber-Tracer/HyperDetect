"""
Creates the socket HyperDbg logs to
"""

import datetime
import socket
import os

SERVER_IP = '0.0.0.0'
LOG_PORT = 8989

def manage_log_connection(conn, file_name):
    with open(file_name, "w") as f:
        timestamp = str(datetime.datetime.now())+","
        f.write(timestamp)
        while True:
            data = conn.recv(1024)
            if not data:
                break  # Connection closed by the client
            timestamp = str(datetime.datetime.now())+","
            data_str = data.decode()
            data_str = data_str.replace("\n", "\n"+ timestamp)
            f.write(data_str)
        f.truncate(f.tell() - len(timestamp))  # Remove the last timestamp

def create_log_socket(filename, client_ip):
    """
    Create a log socket and wait for the client to start logging

    Parameters:
        files_to_send (list): List of file paths to send to the client
        malicious (list): List of booleans indicating if the file is malicious
        log_dir (str): The directory to save the logs to
        duration (int): The duration of each log in minutes
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, LOG_PORT))

    sock.listen(1)
    while True:
        print(f'Waiting for new logs from {client_ip}...')
        connection, client_address = sock.accept()
        if client_address[0] == client_ip:
            manage_log_connection(connection, filename)
            break
        else:
            print(f"Received log from unknown client {client_address[0]}, ignoring...")
    print(f"Client closed log-connection, finished logging {filename}")
    connection.close()
    sock.close()
