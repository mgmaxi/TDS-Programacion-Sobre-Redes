import socket
import json
import pika

# Configuración
HOST = '127.0.0.1'
PORT = 65432
RABBIT_HOST = 'localhost'
QUEUE_NAME = 'task_queue'

def send_to_queue(task):
    """Conecta con RabbitMQ y envía la tarea"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    
    # Declaramos la cola (por si no existe)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    
    # Publicamos el mensaje
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(task),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Hace que el mensaje sea persistente
        ))
    print(f"[Producer] Tarea enviada a RabbitMQ: {task['id']}")
    connection.close()

def start_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Producer escuchando en {HOST}:{PORT}")

    while True:
        client_sock, addr = server.accept()
        print(f"[Producer] Conexión de {addr}")
        
        try:
            data = client_sock.recv(1024).decode('utf-8')
            if data:
                task = json.loads(data)
                
                # 1. Enviar a la cola (RabbitMQ)
                send_to_queue(task)
                
                # 2. Responder al cliente inmediatamente (Ack)
                response = {"status": "queued", "message": "Tarea recibida y encolada"}
                client_sock.sendall(json.dumps(response).encode('utf-8'))
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_sock.close()

if __name__ == "__main__":
    start_socket_server()
