"""
Creates the socket HyperDbg logs to
"""

import datetime
import socket

SERVER_IP = '0.0.0.0'
LOG_PORT = 8989
LOG_START_TIMEOUT = 60
LOG_TIMEOUT = 30

class ClientCrashedException(Exception):

    def __init__(self, minutes_logged):
        self.minutes_logged = minutes_logged
        super().__init__()

def get_minute_diff(timestamp1, timestamp2):
    t1 = datetime.datetime.strptime(timestamp1.strip(','), '%Y-%m-%d %H:%M:%S.%f')
    t2 = datetime.datetime.strptime(timestamp2.strip(','), '%Y-%m-%d %H:%M:%S.%f')
    time_difference = t2 - t1
    return int(time_difference.total_seconds() / 60)


def manage_log_connection(conn, file_name, write_mode='w'):
    conn.settimeout(LOG_TIMEOUT)
    with open(file_name, write_mode) as f:
        initial_timestamp = str(datetime.datetime.now())+","
        timestamp = initial_timestamp
        f.write(initial_timestamp)
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
        except (socket.timeout, ConnectionResetError):
            f.truncate(f.tell() - len(timestamp))  # Remove the last timestamp
            minutes_logged = get_minute_diff(initial_timestamp, timestamp)
            conn.close()
            raise ClientCrashedException(minutes_logged)
        except KeyboardInterrupt:
            pass
        finally:
            conn.close()

def create_log_socket(filename, client_ip, write_mode='w'):
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
    sock.settimeout(LOG_START_TIMEOUT)

    sock.listen(1)
    try:
        print(f'Waiting for new logs from {client_ip}...')
        connection, client_address = sock.accept()
        if client_address[0] == client_ip:
            manage_log_connection(connection, filename, write_mode)
            print(f"Client closed log-connection, finished logging {filename}")
        else:
            print(f"Client {client_address[0]} tried to connect, but it is not the expected client {client_ip}")
    except KeyboardInterrupt:
        print('\nShutting down log server...')
    except Exception as e:
        sock.close()
        raise e
    finally:
        sock.close()
