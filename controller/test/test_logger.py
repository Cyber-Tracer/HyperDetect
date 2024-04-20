import socket
import time
import random as rnd

# This logger was written to simulate the behavior of the HyperDbg tcp log functionality.

def simulate_log(sock, logs_to_send: int, split_msg_rnd: bool = False):
    remaining_msg = ""
    for i in range(logs_to_send):
        message = ""
        # check whether remaining message is not empty
        if remaining_msg:
            message = remaining_msg
            remaining_msg = ""
        
        # message format: pname,pid,tid,syscall,rcx,rdx,r8,r9
        message += f"simulation.exe,{i},{i},1A,{i},{i},{i},{i}\n"
        if split_msg_rnd:
            if rnd.randint(0, 10) == 8:
                # split message at random position
                split_pos = rnd.randint(0, len(message))
                tmp = message[:split_pos]
                remaining_msg = message[split_pos:]
                message = tmp
                print(f"Split occured: {message} | {remaining_msg}")
        sock.sendall(message.encode())
        

# Specify the server's host name and port number
server_host = '0.0.0.0'
server_port = 8989

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's port
server_address = (server_host, server_port)

print("Waiting for connection to log server...")
while True:
    try:
        sock.connect(server_address)
        print("Connection established, start simulation...")
        simulate_log(sock, 1000, split_msg_rnd=True)
        break
    except socket.error as e:
        time.sleep(5)
        print("No connection available, retrying...")