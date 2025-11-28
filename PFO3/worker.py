import pika
import json
import time

RABBIT_HOST = 'localhost'
QUEUE_NAME = 'task_queue'

def save_to_db(task):
    """Simula la conexión con PostgreSQL/S3"""
    print(f"   [DB] Guardando resultado de tarea {task['id']} en base de datos...")
    time.sleep(0.5) # Simula latencia de escritura

def process_task(ch, method, properties, body):
    """Lógica principal del Worker"""
    task = json.loads(body)
    print(f"[Worker] Recibida tarea ID: {task['id']} - Tipo: {task['type']}")
    
    # SIMULACIÓN DE PROCESAMIENTO PESADO
    print("   [Procesando] ...")
    time.sleep(2) 
    
    # PERSISTENCIA (Según tu diagrama)
    save_to_db(task)
    
    print(f"[Worker] Tarea {task['id']} completada.")
    
    # Confirmar a RabbitMQ que la tarea se hizo (Ack)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    
    # Esto asegura que RabbitMQ no le de más de 1 tarea a la vez a este worker
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_task)
    
    print('[*] Worker esperando tareas. Para salir presiona CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
