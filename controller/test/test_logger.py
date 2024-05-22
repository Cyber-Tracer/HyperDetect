import socket
import random as rnd
import time

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

def simulate_client_crash(sock: socket):
    simulate_log(sock, 10)
    print("Simulate client crash...")
    time.sleep(20)
    sock.close()
    
        
def connect_to_log_server(server_host = '0.0.0.0', server_port=8989):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_host, server_port)
    sock.connect(server_address)
    print("Connection to log server established, start simulation...")
    return sock

if __name__ == "__main__":
    sock = connect_to_log_server()
    simulate_log(sock, 10, split_msg_rnd=True)
