import socket

HOST = "127.0.0.1"
PORT = 5000
BUF_SIZE = 4096


def send_message(sock: socket.socket, text: str) -> str:
    """Envía un mensaje (terminado con \n) y retorna la respuesta del servidor."""
    sock.sendall((text + "\n").encode("utf-8"))
    # Leer una línea de respuesta
    data = b""
    while b"\n" not in data:
        chunk = sock.recv(BUF_SIZE)
        if not chunk:
            # Servidor cerró la conexión inesperadamente
            raise ConnectionError("Conexión cerrada por el servidor")
        data += chunk
    return data.decode("utf-8", errors="replace").strip()


def main():
    print("Cliente de chat. Escriba mensajes y presione Enter.")
    print("Para finalizar, escriba: éxito\n")

    try:
        with socket.create_connection((HOST, PORT)) as sock:
            while True:
                texto = input("> ").strip()
                if texto.lower() == "éxito":
                    print("Finalizando cliente…")
                    break
                if not texto:
                    continue
                try:
                    resp = send_message(sock, texto)
                    print(f"[Servidor] {resp}")
                except Exception as e:
                    print(f"Error enviando/recibiendo: {e}")
                    break
    except ConnectionRefusedError:
        print(f"No fue posible conectar con {HOST}:{PORT}. ¿Está el servidor en ejecución?")
    except OSError as e:
        print(f"Error de red: {e}")


if __name__ == "__main__":
    main()
