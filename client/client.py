import socket
import time
import os

# Socket to receive a file from the controller

def receive_file(conn):    
    # Receive the first message containing file size and name
    initial_msg = conn.recv(1024).decode()
    filesize, filename, target_dir = initial_msg.split(':')
    filesize = int(filesize)

    if os.path.isdir(target_dir):
        filename = os.path.join(target_dir, filename)
    else:
        print(f"Invalid dir {target_dir}, saving to current dir.")

    # Open a file for writing
    with open(filename, 'wb') as f:
        bytes_received = 0
        # Receive the rest of the data until we get the full file
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break  # The connection has been closed
            f.write(chunk)
            bytes_received += len(chunk)
    
    if (bytes_received < filesize):
        print(f"Unexpected interrupt, file {filename} incomplete.")
    else:
        print(f"File {filename} received successfully.")

# Specify the server's host name and port number
server_host = '192.168.1.2'
server_port = 9090

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's port
server_address = (server_host, server_port)

print("Waiting for file...")
while True:
    try:
        sock.connect(server_address)
        print("Connection, receiving file...")
        receive_file(sock)
        break
    except socket.error as e:
        time.sleep(5)
        print("No connection available, retrying...")
