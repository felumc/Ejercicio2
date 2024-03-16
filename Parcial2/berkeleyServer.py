import socket
import threading
import time

def get_time_difference(client_time):
    return time.time() - client_time

def handle_client(client_socket, addr):
    client_time = float(client_socket.recv(1024))
    print(f"Received time {client_time} from client {addr}")

    time_diff = get_time_difference(client_time)
    adjusted_time = client_time + time_diff
    print(f"Sending adjusted time {adjusted_time} to client {addr}")

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
