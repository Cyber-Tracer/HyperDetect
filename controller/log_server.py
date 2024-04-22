import socket
import threading
import datetime
import sys
import os

def handle_connection(conn, addr, log_dir):
    # Generate a unique file name for this connection
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"tcp_log_{addr[0]}_{addr[1]}_{timestamp}.log"
    file_name = os.path.join(log_dir, file_name)
    
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
    
    conn.close()
    print(f"Connection with {addr} closed and logged to {file_name}.")

# Specify the server's host name and port number
host = '0.0.0.0'  # Listen on all network interfaces
port = 8989

# Get the path from command line arguments
if len(sys.argv) > 1:
    dir = sys.argv[1]
    if not os.path.exists(dir) or not os.path.isdir(dir):
        print("Invalid path:", dir)
        print("Usage: python log_server.py [directory]")
        sys.exit(1)
    if not os.access(dir, os.W_OK):
        print("Directory is not writable:", dir)
        sys.exit(1)
else:
    dir = os.getcwd()

print('Logging to:', dir)



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
    thread = threading.Thread(target=handle_connection, args=(connection, client_address, dir))
    thread.start()
