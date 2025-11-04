import socket
import threading
import queue

HOST = '0.0.0.0'
PORT = 5000
task_queue = queue.Queue()

def process_task(task_data):
    print(f"Procesando tarea: {task_data}")
    result = f"Resultado de {task_data}"
    return result

def worker():
    while True:
        conn, addr, task_data = task_queue.get()
        result = process_task(task_data)
        conn.sendall(result.encode())
        conn.close()
        task_queue.task_done()

def handle_client(conn, addr):
    data = conn.recv(1024).decode()
    task_queue.put((conn, addr, data))

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")

    for _ in range(5):
        threading.Thread(target=worker, daemon=True).start()

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
