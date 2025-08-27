# Programación sobre redes - Carrera Desarrollo de Software

## Clase 1 - Programación concurrente

Ejercicios

Mejorar el código presentado:

1. "Contando en paralelo"

Parámetros Flexibles: El resuelto tiene el rango que se calculaba con inicio + i y el límite estaba hardcodeado

Configuración Centralizada: Los hilos se creaban manualmente uno por uno.

Manejo Dinámico de Hilos: Join explícito para cada hilo (hilo1.join(), hilo2.join()).

2.  "Sincronización de hilos"

Eliminación de Variables Globales: condicion y resultados son globales.

Uso de wait_for en lugar de while: Bucle while len(resultados) < 2 con wait().

Generación Dinámica de Hilos: Hilos creados manualmente (hilo1, hilo2).

Cálculo Directo con sum(range()): Bucle for para sumar números.

## Clase 2 - Procesos e hilos (Multithreading)

🔹 Hilos (Multithreading)

Permiten ejecutar múltiples tareas dentro de un mismo proceso.

Se ejecutan en paralelo (si hay varios núcleos) o concurrentemente (si hay un solo núcleo).

Uso típico: descargas en segundo plano, procesamiento simultáneo, mantener interfaces gráficas activas.

Ventajas: eficiencia, mejor uso de CPU, interactividad.
Desventajas: problemas de sincronización, mayor complejidad, sobrecarga si se crean demasiados hilos.

🔹 Procesos

Un proceso = un programa en ejecución con su propio espacio de memoria.

Cada proceso es independiente y no accede directamente a la memoria de otro.

Contiene segmentos de memoria: código, datos, pila, heap.

Estados: nuevo, ejecutando, esperando, listo, terminado.

Identificador único: PID.

Comunicación entre procesos (IPC): pipes, memoria compartida, colas de mensajes, sockets.

Ventajas: aislamiento, seguridad.
Desventajas: mayor consumo de recursos, comunicación más lenta que entre hilos.

🔹 Diferencia clave

Proceso: unidad independiente, memoria aislada.

Hilo: subunidad dentro de un proceso, comparte memoria y recursos.

🔹 Glosario de términos clave

Hilo (Thread): unidad mínima de ejecución dentro de un proceso.

Proceso: programa en ejecución con memoria y recursos propios.

PID: identificador único de un proceso.

Heap: memoria dinámica del proceso.

Stack (pila): memoria temporal para funciones y variables locales.

Condición de carrera: error cuando dos hilos acceden al mismo recurso sin control.

IPC (Inter-Process Communication): mecanismos de comunicación entre procesos.

Mapa conceptal: Procesos vs Hilos

![alt text](Procesos-vs-hilos.png)
