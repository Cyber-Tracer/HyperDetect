import socket
from test_logger import connect_to_log_server, simulate_client_crash, simulate_log

# Run server from testing using: python ../start_server.py --input ../input_zipped/V2/benign_MpQuickScan_5min.zip --log_dir test_logs

def simulate_request_next_file(sock):
    sock.sendall("next_file".encode())
    initial_msg = sock.recv(1024).decode()
    filesize, filename = initial_msg.split(';')
    print(f"Simulate receiving file {filename} with size {filesize} bytes")
    filesize = int(filesize)
    bytes_received = 0
    while bytes_received < filesize:
        chunk = sock.recv(1024)
        bytes_received += len(chunk)
        if not chunk:
            print(f"Unexpected interrupt, file {filename} incomplete.")
            break
    print(f"File {filename} received")
    return filesize

def simulate_request_next_log(sock):
    sock.send('next_log'.encode())
    settings_msg = sock.recv(1024).decode()
    malicious, filename, duration_minutes, requires_admin, recovery = settings_msg.split(';')
    print(f"Received following settings for next log: malicious={malicious}, filename={filename}, duration={duration_minutes}, requires_admin={requires_admin}, recovery={recovery}")



# Specify the server's host name and port number
server_host = '0.0.0.0'
server_port = 9090

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's port
server_address = (server_host, server_port)

sock.connect(server_address)
print("Connection established, start simulation...")
while True:
    filesize = simulate_request_next_file(sock)
    if filesize == 0:
        print("No more files to receive, end simulation.")
        break
    simulate_request_next_log(sock)
    log_sock = connect_to_log_server()
    simulate_client_crash(log_sock)
    sock.close()
    print("Simulate client recovery...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    simulate_request_next_file(sock)
    simulate_request_next_log(sock)
    log_sock = connect_to_log_server()
    simulate_log(log_sock, 10, split_msg_rnd=True)
    log_sock.close()

sock.close()
