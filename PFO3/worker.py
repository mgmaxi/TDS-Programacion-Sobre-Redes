import pika
import time

def callback(ch, method, properties, body):
    tarea = body.decode()
    print(f" [x] Worker procesando: {tarea}")
    
    # Simular trabajo pesado
    time.sleep(2)
    result = f"Resultado procesado de {tarea}"
    
    # AQUÍ es donde iría el código para guardar en BD (Postgres/S3)
    print(f" [V] Guardado en BD: {result}")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print(' [*] Worker esperando tareas via RabbitMQ. CTRL+C para salir')
    channel.start_consuming()

if __name__ == "__main__":
    main()
