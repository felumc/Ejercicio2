import numpy as np
import matplotlib.pyplot as plt
import random

# Let's update the script to add a delay to the receiving time to avoid parallel lines

class Process:
    def __init__(self, id):
        self.id = id
        self.time = 0
        self.events = []

    def send_message(self, receiver):
        self.time += random.randint(1, 5)  # Increment time by a random amount to simulate work
        message_time = self.time  # The timestamp at the moment of sending
        self.events.append(('send', message_time, receiver.id))
        # Introduce a delay for the message to be received
        delay = random.randint(1, 5)
        receiver.receive_message(self, message_time, delay)

    def receive_message(self, sender, message_time, delay):
        receive_time = max(self.time, message_time + delay)
        self.time = receive_time  # Update process time
        self.events.append(('receive', self.time, sender.id))

# Reset the processes
processes = [Process(i) for i in range(5)]

# Simulate a sequence of message passing with delays
processes[0].send_message(processes[1])
processes[1].send_message(processes[2])
processes[2].send_message(processes[0])
processes[3].send_message(processes[4])
processes[4].send_message(processes[3])
processes[1].send_message(processes[3])
processes[2].send_message(processes[1])
processes[0].send_message(processes[4])

# Plotting the events with communication lines and delays
fig, ax = plt.subplots(figsize=(12, 8))

# Drawing events and message lines with delays
for process in processes:
    times = [event[1] for event in process.events]
    events = [event[0] for event in process.events]
    ax.plot(times, [process.id] * len(times), 'o-', label=f'Process {process.id}')

    for event, time in zip(events, times):
        ax.text(time, process.id, str(time), fontsize=8, ha='center')

# Draw communication lines with delays
for process in processes:
    for event in process.events:
        if event[0] == 'send':
            # Find the corresponding receive event
            receiver = processes[event[2]]
            receive_events = [e for e in receiver.events if e[0] == 'receive' and e[2] == process.id]
            if receive_events:
                receive_event = receive_events[0]
                send_time = event[1]
                receive_time = receive_event[1]
                # Draw a line with arrowhead representing the delay
                ax.annotate("",
                            xy=(receive_time, receiver.id), xycoords='data',
                            xytext=(send_time, process.id), textcoords='data',
                            arrowprops=dict(arrowstyle="->", lw=1.5, color="red", shrinkA=5, shrinkB=5),
                            )

# Set the plot aesthetics
ax.set_yticks([p.id for p in processes])
ax.set_yticklabels([f'Process {p.id}' for p in processes])
ax.set_xlabel('Time')
ax.set_title('Communication between processes with delays')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

