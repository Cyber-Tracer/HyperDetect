import socket
import time
import os
import zipfile

class ReceiveFileException(Exception):
    pass

class NoFilesException(Exception):
    pass


def receive_file(conn, target_dir):    
    # Receive the first message containing file size and name
    initial_msg = conn.recv(1024).decode()
    filesize, filename = initial_msg.split(';')
    filesize = int(filesize)

    if filesize == 0:
        raise NoFilesException("No files to receive.")

    filename = os.path.join(target_dir, filename)

    # Open a file for writing
    with open(filename, 'wb') as f:
        bytes_received = 0
        # Receive the rest of the data until we get the full file
        while bytes_received < filesize:
            chunk = conn.recv(1024)
            f.write(chunk)
            bytes_received += len(chunk)
            if not chunk:
                raise ReceiveFileException(f"Unexpected interrupt, file {filename} incomplete.")
        
    
    return filename

def extract_zip(filename):
    dst_dir = os.path.dirname(filename)
    dst_dir = os.path.join(dst_dir, os.path.basename(filename).split('.')[0])
    os.makedirs(dst_dir, exist_ok=True)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(dst_dir)
    os.remove(filename)
    return dst_dir
