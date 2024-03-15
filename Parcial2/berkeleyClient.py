import socket
import time

def adjust_time(server_host, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, server_port))
        s.sendall(str(time.time()).encode())
        time_diff = float(s.recv(1024))
        adjusted_time = time.time() + time_diff
        # Set system time here (requires admin privileges and platform-specific code)
        print(f"Adjusted Time: {adjusted_time}")

adjust_time('175.1.52.87', 12345)
