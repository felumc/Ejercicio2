import numpy as np
import matplotlib.pyplot as plt
import random

# Define a class to represent a process
class Process:
    def __init__(self, id):
        self.id = id  # Unique identifier for the process
        self.time = 0  # Current time for the process
        self.events = []  # List of events (send or receive messages)

    # Method to simulate sending a message from this process to a receiver process
    def send_message(self, receiver):
        self.time += random.randint(1, 5)  # Simulate work by incrementing time randomly
        message_time = self.time  # The time at which the message is sent
        self.events.append(('send', message_time, receiver.id))  # Log the send event
        delay = random.randint(1, 5)  # Simulate network delay
        receiver.receive_message(self, message_time, delay)  # The receiver process receives the message

    # Method to simulate receiving a message by this process
    def receive_message(self, sender, message_time, delay):
        receive_time = max(self.time, message_time + delay)  # The time at which the message is received
        self.time = receive_time  # Update the process time
        self.events.append(('receive', self.time, sender.id))  # Log the receive event

# Create 5 processes
processes = [Process(i) for i in range(5)]

# Simulate a sequence of message passing with delays
for i in range(4):
    processes[i].send_message(processes[i + 1])
processes[4].send_message(processes[3])
processes[1].send_message(processes[3])
processes[2].send_message(processes[1])
processes[0].send_message(processes[4])

# Create a plot to visualize the events
fig, ax = plt.subplots(figsize=(12, 8))

# Draw the events and the message lines with delays
for process in processes:
    times = [event[1] for event in process.events]  # Extract the times of the events
    events = [event[0] for event in process.events]  # Extract the types of the events
    ax.plot(times, [process.id] * len(times), 'o-', label=f'Process {process.id}')  # Plot the events
    for event, time in zip(events, times):
        ax.text(time, process.id, str(time), fontsize=8, ha='center')  # Annotate the time of the events

# Draw the communication lines with delays
for process in processes:
    for event in process.events:
        if event[0] == 'send':
            receiver = processes[event[2]]  # Find the receiver process
            receive_events = [e for e in receiver.events if e[0] == 'receive' and e[2] == process.id]  # Find the corresponding receive event
            if receive_events:
                receive_event = receive_events[0]
                send_time = event[1]
                receive_time = receive_event[1]
                ax.annotate("",  # Draw an arrow from the send event to the receive event
                            xy=(receive_time, receiver.id), xycoords='data',
                            xytext=(send_time, process.id), textcoords='data',
                            arrowprops=dict(arrowstyle="->", lw=1.5, color="red", shrinkA=5, shrinkB=5),
                            )

# Set the plot aesthetics
ax.set_yticks([p.id for p in processes])  # Set the y-ticks to the process ids
ax.set_yticklabels([f'Process {p.id}' for p in processes])  # Label the y-ticks with the process ids
ax.set_xlabel('Time')  # Label the x-axis
ax.set_title('Communication between processes with delays')  # Set the title of the plot
plt.legend()  # Show the legend
plt.grid(True)  # Show the grid
plt.tight_layout()  # Adjust the layout
plt.show()  # Display the plot