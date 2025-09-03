# PFO 2 – Sistema de Gestión de Tareas (API + SQLite)

---

## Instalación y ejecución

```bash
# 1) Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Ejecutar el servidor
python servidor.py
# El servicio quedará en http://127.0.0.1:5000
```

---

## Endpoints

### 1) Registro de Usuarios — `POST /registro`

**Body JSON**

```json
{ "usuario": "maxi", "contraseña": "1234" }
```

**Respuestas**

- `201 Created` → usuario creado
- `409 Conflict` → usuario ya existe
- `400 Bad Request` → faltan campos

### 2) Inicio de Sesión — `POST /login`

**Body JSON**

```json
{ "usuario": "maxi", "contraseña": "1234" }
```

**Respuestas**

- `200 OK` → credenciales válidas
- `401 Unauthorized` → credenciales inválidas
- `400 Bad Request` → faltan campos

### 3) Bienvenida (con auth) — `GET /tareas`

**Ejemplo con `curl`:**

```bash
# Registro
curl -s -X POST http://127.0.0.1:5000/registro \
  -H "Content-Type: application/json" \
  -d '{"usuario":"maxi","contraseña":"1234"}'

# Login
curl -s -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"maxi","contraseña":"1234"}'

# Acceso a /tareas con auth
curl -u maxi:1234 http://127.0.0.1:5000/tareas
```
