import socket
import threading
import datetime
import time

def handle_connection(conn, addr):
    # Generate a unique file name for this connection
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"tcp_log_{addr[0]}_{addr[1]}_{timestamp}.log"
    
    with open(file_name, "wb") as f:
        while True:
            data = conn.recv(1024)
            timestamp = str(datetime.datetime.now())+","
            if not data:
                break  # Connection closed by the client
            f.write(timestamp.encode() + data)
    
    conn.close()
    print(f"Connection with {addr} closed and logged to {file_name}.")

# Specify the server's host name and port number
host = '0.0.0.0'  # Listen on all network interfaces
port = 8989

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (host, port)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Get the IP address of the current system
ip_address = sock.getsockname()[0]
print('IP address:', ip_address)

while True:
    print('Waiting for a connection...')
    connection, client_address = sock.accept()
    thread = threading.Thread(target=handle_connection, args=(connection, client_address))
    thread.start()