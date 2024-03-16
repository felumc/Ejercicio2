import socket
import time
from threading import Thread

def handle_client_connection(client_socket):
    # Receive the request (not used in this simple example)
    _ = client_socket.recv(1024)
    
    # Send back the current server time
    current_time = str(time.time())
    print(f"Sending current time: {current_time}")
    client_socket.sendall(current_time.encode('utf-8'))
    client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # Max number of queued connections

    print(f"Server listening on {host}:{port}")

    while True:
        client_sock, address = server.accept()
        print(f"Accepted connection from {address[0]}:{address[1]}")
        client_handler = Thread(target=handle_client_connection,
                                args=(client_sock,))
        client_handler.start()

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 12345
    start_server(HOST, PORT)
