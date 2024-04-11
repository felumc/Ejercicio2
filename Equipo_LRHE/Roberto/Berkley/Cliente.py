import socket
import time

def solicitar_tiempo_servidores(servidores):
    tiempos = []
    for servidor in servidores:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(servidor)
            s.send(b'SolicitarTiempo')
            tiempo_servidor = float(s.recv(1024).decode())
            tiempos.append(tiempo_servidor)
    return tiempos

def ajustar_reloj_local(tiempos):
    tiempo_promedio = sum(tiempos) / len(tiempos)
    ajuste = tiempo_promedio - time.time()
    return ajuste

def main():
    # Direcciones y puertos de los servidores
    servidores = [('127.0.0.1', 12345), ('127.0.0.1', 12346), ('127.0.0.1', 12347)]
    # Solicitar tiempos a los servidores
    tiempos_servidores = solicitar_tiempo_servidores(servidores)
    # Ajustar el reloj local
    ajuste = ajustar_reloj_local(tiempos_servidores)
    print("Ajuste de reloj local:", ajuste)

if __name__ == "__main__":
    main()
