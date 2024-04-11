import socket
import time

def obtener_tiempo_servidor(host, puerto):
    # Conectarse al servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, puerto))
        # Enviar solicitud de tiempo
        s.send(b'SolicitarTiempo')
        # Recibir tiempo del servidor
        tiempo_servidor = float(s.recv(1024).decode())
    return tiempo_servidor

def obtener_diferencia_local(tiempo_servidor):
    # Obtener el tiempo local en el cliente
    tiempo_local = time.time()
    # Calcular la diferencia de tiempo
    diferencia = tiempo_servidor - tiempo_local
    return diferencia

def main():
    # Dirección y puerto del servidor
    host = '127.0.0.1'
    puerto = 12345
    # Obtener tiempo del servidor
    tiempo_servidor = obtener_tiempo_servidor(host, puerto)
    # Calcular la diferencia de tiempo
    diferencia = obtener_diferencia_local(tiempo_servidor)
    print("Diferencia de tiempo con el servidor:", diferencia)

if __name__ == "__main__":
    main()
