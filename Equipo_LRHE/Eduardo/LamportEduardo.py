from threading import Thread, Lock
import time
import matplotlib.pyplot as plt

class LamportClock:
    def __init__(self):
        self.clock = [0, 0]  # Un reloj por cada proceso
        self.history = [[0, 0]]  # Historial de relojes por cada proceso
        self.lock = Lock()

    def tick(self, process_id):
        with self.lock:
            self.clock[process_id] += 1
            self.history.append(self.clock.copy())
            return self.clock[process_id]

    def update(self, process_id, received_time):
        with self.lock:
            self.clock[process_id] = max(self.clock[process_id], received_time) + 1
            self.history.append(self.clock.copy())
            return self.clock[process_id]

def process_1(clock):
    time.sleep(1)
    timestamp = clock.tick(0)
    print("Process 1 - Event occurred at time:", timestamp)

def process_2(clock):
    time.sleep(2)
    timestamp = clock.tick(1)
    print("Process 2 - Event occurred at time:", timestamp)

if __name__ == "__main__":
    clock = LamportClock()

    thread1 = Thread(target=process_1, args=(clock,))
    thread2 = Thread(target=process_2, args=(clock,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    # Crear la gráfica dinámica de movimiento de procesos
    plt.figure(figsize=(10, 6))
    for i in range(2):  # Iterar sobre cada proceso
        times = [step[i] for step in clock.history]  # Obtener los tiempos para el proceso i
        plt.plot(times, label=f'Process {i+1}', marker='o')

    plt.xlabel('Time Steps')
    plt.ylabel('Lamport Clock Value')
    plt.title('Lamport Clock Execution')
    plt.legend()
    plt.grid(True)
    plt.show()
