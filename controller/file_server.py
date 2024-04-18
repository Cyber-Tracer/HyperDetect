import os
import socket

def send_file(filepath, client_socket, target_dir):
    # Get the file size
    filesize = os.path.getsize(filepath)
    filename = os.path.basename(filepath)
    
    # Send the filesize and filename
    client_socket.send(f"{filesize};{filename};{target_dir}".encode())
    
    # Open the file and send its content
    with open(filepath, 'rb') as f:
        # Read and send the file in chunks
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break  # File sending is done
            client_socket.sendall(bytes_read)

def read_file_from_input():
    while True:
        filename = input("Enter the name of the file to send: ")
        if os.path.exists(filename):
            return filename
        else:
            print("File not found, try again.")

# Specify the server's host name and port number
host = '0.0.0.0'  # Listen on all network interfaces
port = 9090

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


print('Waiting for a connection...')
connection, client_address = sock.accept()
print("Connection established with ", client_address)
filename = read_file_from_input()
target_dir = input("Enter the target directory (default = C:\HyperDbg\client): ")
send_file(filename, connection, target_dir)
print("File sent successfully.")
connection.close()
sock.close()


