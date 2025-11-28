import socket
import json
import pika

HOST = '0.0.0.0'
PORT = 5000

# Configuración RabbitMQ
def enviar_a_cola(mensaje):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=mensaje,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[*] Servidor Productor escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Conexión de {addr}")
            data = conn.recv(1024).decode()
            if data:
                # Enviar solo los DATOS a RabbitMQ, no la conexión
                print(f"Encolando tarea: {data}")
                enviar_a_cola(data) 
                
                # Responder al cliente que ya se tomó el pedido
                conn.sendall(b"Tarea recibida y encolada exitosamente.")

if __name__ == "__main__":
    main()
