"""
Provides functions to send files to a client.
"""

import os

def send_no_files(connection):
    """
    When the client requested files, but we do not have any more to send, send a message to the client indicating that no more files are available.
    """
    connection.send("0;NONE".encode())

def send_file(connection, filepath):
    """
    Send a file to the client over the connection.
    """
    # Get the file size
    filesize = os.path.getsize(filepath)
    filename = os.path.basename(filepath)
    
    # Send the filesize and filename
    connection.send(f"{filesize};{filename}".encode())
    
    # Open the file and send its content
    with open(filepath, 'rb') as f:
        # Read and send the file in chunks
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break  # File sending is done
            connection.sendall(bytes_read)


