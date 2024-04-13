import socket
import threading
import time

class BullyNode:
    def __init__(self, node_id, port, nodes_info):
        self.node_id = node_id
        self.port = port
        self.nodes_info = nodes_info  # Dictionary of node_id: port
        self.coordinator = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', port))
        self.alive = True

    def send_message(self, message, port):
        self.socket.sendto(message.encode(), ('localhost', port))

    def receive_message(self):
        while self.alive:
            message, _ = self.socket.recvfrom(1024)
            message = message.decode()
            print(f"Node {self.node_id} received: {message}")
            self.process_message(message)

    def process_message(self, message):
        msg_type, sender_id = message.split(',')
        sender_id = int(sender_id)

        if msg_type == 'ELECTION':
            if sender_id < self.node_id:
                self.send_message(f'ANSWER,{self.node_id}', self.nodes_info[sender_id])
                self.start_election()
        elif msg_type == 'COORDINATOR':
            self.coordinator = sender_id
            print(f"Node {self.node_id} acknowledges new coordinator: {self.coordinator}")

    def start_election(self):
        responses = False
        for node_id, port in self.nodes_info.items():
            if node_id > self.node_id:
                self.send_message(f'ELECTION,{self.node_id}', port)
                responses = True

        if not responses:
            self.announce_coordinator()

    def announce_coordinator(self):
        self.coordinator = self.node_id
        for node_id, port in self.nodes_info.items():
            if node_id != self.node_id:
                self.send_message(f'COORDINATOR,{self.node_id}', port)

    def run(self):
        threading.Thread(target=self.receive_message).start()

def main():
    nodes_info = {1: 5001, 2: 5002, 3: 5003}
    node_id = int(input("Enter this node's ID (1, 2, or 3): "))
    node = BullyNode(node_id, nodes_info[node_id], nodes_info)
    node.run()

    while True:
        cmd = input("Enter 'start' to initiate an election or 'exit' to quit: ")
        if cmd == 'start':
            node.start_election()
        elif cmd == 'exit':
            node.alive = False
            break

if __name__ == "__main__":
    main()