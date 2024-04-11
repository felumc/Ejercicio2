import socket
import threading
import time

# Variable global para la marca de tiempo del cliente
marca_tiempo_cliente = 0

def enviar_mensaje(servidor_socket, mensaje):
    global marca_tiempo_cliente
    # Incrementar la marca de tiempo del cliente
    marca_tiempo_cliente += 1
    marca_tiempo = marca_tiempo_cliente
    # Enviar el mensaje junto con la marca de tiempo
    mensaje_con_tiempo = f"{mensaje}:{marca_tiempo}".encode()
    servidor_socket.send(mensaje_con_tiempo)

def recibir_mensaje(servidor_socket):
    while True:
        # Recibir mensaje del servidor
        mensaje = servidor_socket.recv(1024).decode()
        # Extraer la marca de tiempo del mensaje
        mensaje, marca_tiempo = mensaje.split(':')
        marca_tiempo = int(marca_tiempo)
        # Actualizar la marca de tiempo del cliente
        global marca_tiempo_cliente
        marca_tiempo_cliente = max(marca_tiempo_cliente, marca_tiempo) + 1
        print(f"Mensaje recibido: {mensaje} (marca de tiempo: {marca_tiempo})")

def main():
    # Dirección y puerto del servidor
    host = '127.0.0.1'
    puerto = 12345

    # Crear un socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        # Conectarse al servidor
        cliente_socket.connect((host, puerto))
        print("Conectado al servidor.")

        # Iniciar un hilo para recibir mensajes del servidor
        recibir_hilo = threading.Thread(target=recibir_mensaje, args=(cliente_socket,))
        recibir_hilo.start()

        # Enviar algunos mensajes al servidor
        for i in range(5):
            time.sleep(1)
            enviar_mensaje(cliente_socket, f"Mensaje {i+1}")

if __name__ == "__main__":
    main()
