import socket
import sqlite3
import threading
from datetime import datetime
from typing import Tuple, Optional

# Configuración y constantes

HOST = "127.0.0.1"   # localhost
PORT = 5000          # Puerto requerido
DB_PATH = "mensajes.db" # Base de datos SQLite
BACKLOG = 5          # Tamaño de la cola de conexiones pendientes
BUF_SIZE = 4096      # Tamaño del buffer de recepción

# Inicialización de la Base de DB

def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
            """
        )
        conn.commit()
        return conn
    except sqlite3.Error as e:
        # Error de acceso/creación a la DB
        raise RuntimeError(f"Error inicializando DB: {e}") from e

# Persistencia de datos en SQLite

def save_message(conn: sqlite3.Connection, contenido: str, fecha_envio: str, ip_cliente: str) -> int:
    """Inserta un mensaje y retorna el id generado."""
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO mensajes(contenido, fecha_envio, ip_cliente)
            VALUES(?, ?, ?)
            """,
            (contenido, fecha_envio, ip_cliente),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"[DB] Error guardando mensaje: {e}")
        raise

# Gestión de sockets

def init_server_socket(host: str = HOST, port: int = PORT, backlog: int = BACKLOG) -> socket.socket:
    """Inicializa el socket TCP/IP de escucha.
    """
    try:
        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Permite reutilizar la dirección rápidamente tras reinicios del servidor
        srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv_sock.bind((host, port)) 
        srv_sock.listen(backlog)
        print(f"[SRV] Escuchando en {host}:{port} ...")
        return srv_sock
    except OSError as e:
        # Manejo específico de errores de red/puerto ocupado
        raise RuntimeError(f"No se pudo iniciar el servidor en {host}:{port}: {e}") from e

# Manejo de conexiones (Hilos)

def handle_client(conn_db: sqlite3.Connection, client_sock: socket.socket, addr: Tuple[str, int]):
    """Atiende a un cliente: recibe mensajes, persiste y confirma.
"""
    ip, port = addr
    print(f"[CLI] Conectado: {ip}:{port}")
    with client_sock:
        try:
            # Bucle de recepción: el cliente puede enviar múltiples líneas
            buffer = b""
            while True:
                chunk = client_sock.recv(BUF_SIZE)
                if not chunk:
                    # El cliente cerró la conexión
                    print(f"[CLI] {ip}:{port} desconectado (EOF)")
                    break
                buffer += chunk
                # Procesar por líneas: mensajes terminados en \n
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    mensaje = line.decode("utf-8", errors="replace").strip()
                    if not mensaje:
                        continue

                    # Timestamp en ISO 8601 con segundos
                    ts = datetime.now().isoformat(timespec="seconds")

                    # Persistir en DB
                    try:
                        save_message(conn_db, mensaje, ts, ip)
                    except sqlite3.Error:
                        # Si falla la DB, informar al cliente sin tumbar el servidor
                        err_msg = "Error interno al guardar el mensaje"
                        client_sock.sendall((err_msg + "\n").encode("utf-8"))
                        continue

                    # Enviar confirmación al cliente
                    respuesta = f"Mensaje recibido: {ts}\n"
                    client_sock.sendall(respuesta.encode("utf-8"))
        except ConnectionResetError:
            print(f"[CLI] {ip}:{port} conexión reiniciada por el peer")
        except Exception as e:
            print(f"[CLI] Error inesperado con {ip}:{port}: {e}")
        finally:
            print(f"[CLI] Cerrando conexión con {ip}:{port}")


def accept_loop(conn_db: sqlite3.Connection, srv_sock: socket.socket):
    """Bucle principal de aceptación de conexiones entrantes."""
    try:
        while True:
            client_sock, addr = srv_sock.accept()
            # Hilo por cliente para permitir concurrencia simple
            t = threading.Thread(target=handle_client, args=(conn_db, client_sock, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n[SRV] Interrupción por teclado. Cerrando...")
    except Exception as e:
        print(f"[SRV] Error en accept_loop: {e}")

# main()

def main():
    # 1) Inicializar DB
    try:
        conn_db = init_db(DB_PATH)
        print(f"[DB] Base lista en {DB_PATH}")
    except RuntimeError as e:
        print(str(e))
        return

    # 2) Inicializar socket de servidor
    try:
        srv_sock = init_server_socket(HOST, PORT, BACKLOG)
    except RuntimeError as e:
        print(str(e))
        conn_db.close()
        return

    # 3) Aceptar conexiones
    try:
        accept_loop(conn_db, srv_sock)
    finally:
        # Cierre ordenado de recursos
        try:
            srv_sock.close()
        except Exception:
            pass
        try:
            conn_db.close()
        except Exception:
            pass
        print("[SRV] Recursos liberados. Fin.")


if __name__ == "__main__":
    main()
