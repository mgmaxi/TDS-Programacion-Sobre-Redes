
#Problema 2: Sincronización de hilos

#Crea un programa que simule dos hilos sumando números. 
# Ambos hilos deben sumar números del 1 al 5, pero no deben imprimir el resultado de la suma hasta que ambos hayan completado la suma de los 5 números. 
# Utiliza una variable de condición para asegurar que los resultados solo se impriman una vez que ambos hilos hayan terminado su tarea.
""" 
import threading
 
# Variable de condición para sincronización
condicion = threading.Condition()
 
# Variables globales
resultados = []
 
def sumar_numeros(nombre):
    total = 0
    for i in range(1, 6):
        total += i
    with condicion:
        resultados.append(f"{nombre} sumó: {total}")
        condicion.notify_all()  # Notificar que se ha terminado la suma
 
def imprimir_resultados():
    with condicion:
        while len(resultados) < 2:
            condicion.wait()  # Esperar hasta que ambos hilos hayan terminado
        for resultado in resultados:
            print(resultado)
 
hilo1 = threading.Thread(target=sumar_numeros, args=("Hilo 1",))
hilo2 = threading.Thread(target=sumar_numeros, args=("Hilo 2",))
 
hilo1.start()
hilo2.start()
 
# Imprimir los resultados una vez que ambos hilos hayan terminado
imprimir_resultados() """

#Código optimizado y mejor estructurado según lo solicitado en el tp del aula virtual

#Eliminación de Variables Globales: condicion y resultados son globales.
#Uso de wait_for en lugar de while: Bucle while len(resultados) < 2 con wait().
#Generación Dinámica de Hilos: Hilos creados manualmente (hilo1, hilo2).
#Cálculo Directo con sum(range()): Bucle for para sumar números.

import threading

def sumar_numeros():
    return sum(range(1, 6))

resultados = []
condicion = threading.Condition()

def worker(nombre):
    total = sumar_numeros()
    with condicion:
        resultados.append(f"{nombre} sumó: {total}")
        condicion.notify_all()

# Generación dinámica de hilos
nombres = ["Hilo 1", "Hilo 2"]
hilos = [threading.Thread(target=worker, args=(n,)) for n in nombres]

for h in hilos:
    h.start()

# Uso de wait_for en lugar de while
with condicion:
    condicion.wait_for(lambda: len(resultados) == len(nombres))

for r in resultados:
    print(r)

for h in hilos:
    h.join()
