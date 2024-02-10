
import threading
import socket
import os

# Read the content of the files
hostList = ['175.1.36.225', '175.1.32.222', '175.1.33.190', '175.1.35.38']
hostHendrick = '175.1.36.225'
hostLalo = '175.1.32.222'
hostRobert = '175.1.33.190'
hostLuis = '175.1.35.38'

def send_file(host, file_path):  # Replace with the IP address of the receiving Mac
    port = 12345  # Use the same port number as in the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    file_name = os.path.basename(file_path)
    client_socket.send(file_name.encode('utf-8') + b'\x00')
    
    with open(file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    print("File sent successfully")
    client_socket.close()

for i in hostList:
    send_file(i, 'hendrick.txt')