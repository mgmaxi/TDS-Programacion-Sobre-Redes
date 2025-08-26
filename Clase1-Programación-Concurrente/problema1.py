#Problema 1: Contando en paralelo

#Escribe un programa en Python que cree dos hilos.
# El primer hilo debe contar los números del 1 al 5, mientras que el segundo hilo debe contar los números del 6 al 10. 
# Los números de cada hilo deben imprimirse de forma concurrente, pero no necesariamente en el mismo orden.


""" import threading
import time
 
def contar_numeros(nombre, inicio, limite):
    for i in range(limite):
        time.sleep(1)  # Simula un trabajo que toma tiempo (1 segundo por número)
        print(f"{nombre} está contando: {inicio + i}")
 
hilo1 = threading.Thread(target=contar_numeros, args=("Hilo 1", 1, 15))
hilo2 = threading.Thread(target=contar_numeros, args=("Hilo 2", 6, 5))
 
hilo1.start()
hilo2.start()
 
hilo1.join()
hilo2.join()
 
print("¡Contador completo!") """


#Código optimizado y mejor estructurado según lo solicitado en el tp del aula virtual

#Parámetros Flexibles: El resuelto tiene el rango que se calculaba con inicio + i y el límite estaba hardcodeado
#Configuración Centralizada: Los hilos se creaban manualmente uno por uno.
#Manejo Dinámico de Hilos: Join explícito para cada hilo (hilo1.join(), hilo2.join())

import threading
import time

# Configuración centralizada: (nombre, inicio, fin)
configuraciones = [
    ("Hilo 1", 1, 5),
    ("Hilo 2", 6, 10),
]

def contar_numeros(nombre, inicio, fin):
    # Parámetros flexibles: rango incluye(inicio, fin + 1) con un argumento flexible, diferente al hardcodeado anteriromente.
    for n in range(inicio, fin + 1):
        time.sleep(1)
        print(f"{nombre} está contando: {n}")

# Manejo dinámico de hilos (creación y join en bucles)
hilos = [threading.Thread(target=contar_numeros, args=cfg) for cfg in configuraciones]

for h in hilos:
    h.start()

for h in hilos:
    h.join()

print("¡Contador completo!")

