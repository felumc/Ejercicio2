import socket
import time
from datetime import datetime

def get_server_time():
    # Replace with your server's host and port
    server_host = '175.1.52.87'
    server_port = 12345
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, server_port))
        t0 = time.time()  # Local time before request
        print(f"Local time before request: {datetime.fromtimestamp(t0)}")
        s.sendall(b"Time Request")
        server_time = float(s.recv(1024))
        t1 = time.time()  # Local time after response
        print(f"Local time after response: {datetime.fromtimestamp(t1)}")

    return server_time, t0, t1

def synchronize_time():
    server_time, t0, t1 = get_server_time()
    rtt = t1 - t0
    print(f"Round trip time: {datetime.fromtimestamp(rtt)}")
    adjusted_time = server_time + (rtt / 2)
    # Set system time here (requires admin privileges and platform-specific code)
    print(f"Adjusted Time: {datetime.fromtimestamp(adjusted_time)}")

synchronize_time()
