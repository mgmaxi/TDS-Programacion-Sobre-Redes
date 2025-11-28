import socket
import json

HOST = '127.0.0.1'
PORT = 65432

def enviar_tarea(tarea_id, tipo):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        task = {"id": tarea_id, "type": tipo, "content": "datos_ejemplo"}
        s.sendall(json.dumps(task).encode('utf-8'))
        
        # Esperamos confirmación de recepción (no el resultado final)
        data = s.recv(1024)
        print(f"[Cliente] Respuesta del servidor: {data.decode('utf-8')}")

if __name__ == "__main__":
    for i in range(1, 4):
        enviar_tarea(i, "procesamiento_imagen")
