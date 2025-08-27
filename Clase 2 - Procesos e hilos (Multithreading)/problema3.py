import threading
import time

def contar(inicio, fin):
    for i in range(inicio, fin + 1):
        print(i)
        time.sleep(0.2)  # pequeña pausa para simular concurrencia

# Crear hilos
hilo1 = threading.Thread(target=contar, args=(1, 5))
hilo2 = threading.Thread(target=contar, args=(6, 10))

# Iniciar hilos
hilo1.start()
hilo2.start()

# Esperar que ambos terminen
hilo1.join()
hilo2.join()
