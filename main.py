
import threading
import socket
import os

# Read the content of the files

hostHendrick = '175.1.36.225'
hostLalo = '175.1.32.222'
hostRobert = '175.1.33.190'
hostLuis = '175.1.35.38'

#open my socket to receive files non stop
def receive_file():
    host = '175.1.35.38'
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

#open my socket to send files to the other computers

def send_file(host, file_name):
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print(f"Connection to {host} refused")
        return

    with open(file_name, 'rb') as file:
        # Send the filename
        client_socket.send(os.path.basename(file_name).encode('utf-8') + b'\x00')

        # Send the file contents
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.send(data)

    print(f"File {file_name} sent successfully")
    client_socket.close()


receive_thread = threading.Thread(target=receive_file)
receive_thread.start()

mandar = int(input("Press Enter to send file"))
send_file(hostHendrick, 'hendrick.txt')
send_file(hostLalo, 'lalo.txt')
send_file(hostRobert, 'robert.txt')
send_file(hostLuis, 'luis.txt')

receive_thread.join()