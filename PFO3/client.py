import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

def send_task(task):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.sendall(task.encode())
        result = s.recv(1024).decode()
        print(f"Respuesta del servidor: {result}")

if __name__ == "__main__":
    tarea = input("Ingrese tarea a enviar: ")
    send_task(tarea)
