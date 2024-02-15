import socket


hostHendrick = '175.1.36.225'
hostLalo = '175.1.42.68'
hostRobert = '175.1.33.190'
hostLuis = '175.1.35.211'

def receive_file(host): # Replace with the IP address of the receiving Mac
    port = 12345  # Choose a port number

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Allow up to 5 simultaneous connections

    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        try:
            # Receive the filename from the client
            file_name = b''
            while True:
                byte = conn.recv(1)
                if not byte or byte == b'\x00':
                    break
                file_name += byte

            file_name = file_name.decode('utf-8', errors='replace').strip()
        except UnicodeDecodeError as e:
            print(f"Error decoding filename: {e}")
            continue

        with open(file_name, 'wb') as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)

        print(f"File {file_name} received successfully")
        conn.close()

if __name__ == "__main__":
    receive_file(hostLuis)