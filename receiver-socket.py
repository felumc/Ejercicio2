import os
import socket

hostHendrick = '175.1.37.112'
hostLalo = '175.1.42.68'
hostRobert = '175.1.46.120'
hostLuis = '175.1.35.211'

def receive_file(host):
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        try:
            file_name = b''
            while True:
                byte = conn.recv(1)
                if not byte or byte == b'\x00':
                    break
                file_name += byte

            file_name = file_name.decode('utf-8', errors='replace').strip()
            extension = os.path.splitext(file_name)[1].lower()

            if extension in ['.mp4', '.avi', '.mkv', '.MOV', '.heic', '.jpg', '.png', '.gif', '.mp3']:
                folder = 'mutimedia'
            else:
                folder = 'datos'

        except UnicodeDecodeError as e:
            print(f"Error decoding filename: {e}")
            continue

        file_path = os.path.join(folder, file_name)

        with open(file_path, 'wb') as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)

        print(f"File {file_name} received successfully and saved to {file_path}")
        conn.close()

if __name__ == "__main__":
    receive_file(hostRobert)
