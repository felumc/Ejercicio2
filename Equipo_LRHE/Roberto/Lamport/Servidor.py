import socket
import threading
import time

# Variable global para la marca de tiempo del servidor
marca_tiempo_servidor = 0

def manejar_cliente(cliente_socket, cliente_direccion):
    global marca_tiempo_servidor
    while True:
        # Recibir mensaje del cliente
        mensaje = cliente_socket.recv(1024).decode()
        # Incrementar la marca de tiempo del servidor
        marca_tiempo_servidor += 1
        marca_tiempo = marca_tiempo_servidor
        # Enviar el mensaje de vuelta con la marca de tiempo del servidor
        mensaje_con_tiempo = f"{mensaje}:{marca_tiempo}".encode()
        cliente_socket.send(mensaje_con_tiempo)
        print(f"Mensaje enviado a {cliente_direccion}: {mensaje} (marca de tiempo: {marca_tiempo})")

def main():
    # Dirección y puerto del servidor
    host = '127.0.0.1'
    puerto = 12345

    # Crear un socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        # Enlazar el socket a la dirección y puerto especificados
        servidor_socket.bind((host, puerto))
        # Escuchar conexiones entrantes
        servidor_socket.listen(5)
        print("Servidor escuchando en", host, "puerto", puerto)

        while True:
            # Esperar por una conexión
            cliente_socket, cliente_direccion = servidor_socket.accept()
            print("Conexión establecida desde", cliente_direccion)
            # Iniciar un hilo para manejar la conexión con el cliente
            cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente_socket, cliente_direccion))
            cliente_thread.start()

if __name__ == "__main__":
    main()
