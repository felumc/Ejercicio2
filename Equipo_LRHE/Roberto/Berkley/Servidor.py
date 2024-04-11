import socket
import time

def manejar_conexion(cliente_socket):
    solicitud = cliente_socket.recv(1024).decode()
    if solicitud == 'SolicitarTiempo':
        tiempo_servidor = time.time()
        cliente_socket.send(str(tiempo_servidor).encode())
    else:
        cliente_socket.send('Solicitud no válida')
    cliente_socket.close()

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
            # Manejar la conexión con el cliente
            manejar_conexion(cliente_socket)

if __name__ == "__main__":
    main()
