# Rediseño como Sistema Distribuido (Cliente-Servidor)

## Objetivo

Transformar el sistema en una arquitectura distribuida basada en el modelo Cliente-Servidor, utilizando sockets para la comunicación entre componentes y aplicando buenas prácticas de concurrencia, balanceo de carga y mensajería distribuida.

---

## Consignas

1. **Diseñar un diagrama que incluya:**

   - Clientes (móviles, web).
   - Balanceador de carga (Nginx / HAProxy).
   - Servidores workers (cada uno con su pool de hilos).
   - Cola de mensajes (RabbitMQ) para comunicación entre servidores.
   - Almacenamiento distribuido (PostgreSQL, S3).

2. **Implementar en Python:**
   - Un servidor que reciba tareas por socket y las distribuya a los workers.
   - Un cliente que envíe tareas y reciba los resultados.

---

## Entregables

- Diagrama del sistema distribuido.
- Código fuente del servidor y cliente en un repositorio de GitHub.
