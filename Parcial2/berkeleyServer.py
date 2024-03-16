import socket
import threading
import time
from datetime import datetime

def get_time_difference(client_time):
    return time.time() - client_time

def handle_client(client_socket, client_address):
    client_time = float(client_socket.recv(1024))
    current_time = time.time()
    time_diff = get_time_difference(client_time)
    adjusted_time = current_time + time_diff

    print(f"Client {client_address} Time: {datetime.fromtimestamp(client_time)}")
    print(f"Current Server Time: {datetime.fromtimestamp(current_time)}")
    print(f"Adjusted Time for Client: {datetime.fromtimestamp(adjusted_time)}")

    client_socket.sendall(str(time_diff).encode())
    client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Berkeley Algorithm Master running on {host}:{port}")

    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    start_server('0.0.0.0', 12345)
