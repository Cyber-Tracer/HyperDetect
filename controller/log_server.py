"""
Creates the socket HyperDbg logs to
"""

import datetime
import socket
import os

SERVER_IP = '0.0.0.0'
LOG_PORT = 8989
LOG_TIMEOUT = 60

def manage_log_connection(conn, file_name):
    conn.settimeout(LOG_TIMEOUT)
    with open(file_name, "w") as f:
        timestamp = str(datetime.datetime.now())+","
        f.write(timestamp)
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break  # Connection closed by the client
                timestamp = str(datetime.datetime.now())+","
                data_str = data.decode()
                data_str = data_str.replace("\n", "\n"+ timestamp)
                f.write(data_str)
            f.truncate(f.tell() - len(timestamp))  # Remove the last timestamp
        except KeyboardInterrupt:
            pass
        finally:
            conn.close()

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
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of address, prevent "Address already in use" error
    sock.bind((SERVER_IP, LOG_PORT))

    sock.listen(1)
    try:
        while True:
            print(f'Waiting for new logs from {client_ip}...')
            connection, client_address = sock.accept()
            if client_address[0] == client_ip:
                try:
                    manage_log_connection(connection, filename)
                except TimeoutError:
                    print(f"Client {client_address[0]} timed out")
                break
            else:
                print(f"Received log from unknown client {client_address[0]}, ignoring...")
        print(f"Client closed log-connection, finished logging {filename}")
    except KeyboardInterrupt:
        print('\nShutting down log server...')
    finally:
        sock.close()
