# Programación sobre redes - Carrera Desarrollo de Software

## Clase 1 - PSR-Clase1-Programación-Concurrente

En este espacio van a entregar las mejoras de los problemas "Contando en paralelo" y "Sincronización de hilos", cuyos enunciados se detallan al finalizar el material de esta clase hasta el plazo establecido, y que están resueltos en el foro.

Enumero que pueden mejorar y como esta ahora, ustedes van a proponer como Mejorarlas:

1. "Contando en paralelo"

Parámetros Flexibles: El resuelto tiene el rango que se calculaba con inicio + i y el límite estaba hardcodeado

Configuración Centralizada: Los hilos se creaban manualmente uno por uno.

Manejo Dinámico de Hilos: Join explícito para cada hilo (hilo1.join(), hilo2.join()).

2.  "Sincronización de hilos"

Eliminación de Variables Globales: condicion y resultados son globales.

Uso de wait_for en lugar de while: Bucle while len(resultados) < 2 con wait().

Generación Dinámica de Hilos: Hilos creados manualmente (hilo1, hilo2).

Cálculo Directo con sum(range()): Bucle for para sumar números.
