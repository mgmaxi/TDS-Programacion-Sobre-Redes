import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64decode

DB_PATH = os.environ.get("DB_PATH", "pfo2.sqlite3")

app = Flask(__name__)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        """)
        conn.commit()

init_db()

# --- autenticación  ---
def parse_basic_auth(auth_header: str):
    """
    Devuelve (username, password) si el encabezado es válido; en caso contrario (None, None).
    """
    try:
        if not auth_header or not auth_header.startswith("Basic "):
            return None, None
        encoded = auth_header.split(" ", 1)[1]
        decoded = b64decode(encoded).decode("utf-8")
        if ":" not in decoded:
            return None, None
        username, password = decoded.split(":", 1)
        return username, password
    except Exception:
        return None, None

def verify_user(username: str, password: str) -> bool:
    with get_conn() as conn:
        row = conn.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()
        if not row:
            return False
        return check_password_hash(row["password_hash"], password)

# --- endpoints ---
@app.post("/registro")
def registro():
    """
    Body JSON: {"usuario": "nombre", "contraseña": "1234"}
    Crea el usuario si no existe. Devuelve 201 en caso de éxito.
    """
    data = request.get_json(silent=True) or {}
    username = data.get("usuario")
    password = data.get("contraseña")

    if not username or not password:
        return jsonify({"error": "Faltan campos: 'usuario' y 'contraseña' son obligatorios."}), 400

    pwd_hash = generate_password_hash(password)

    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, pwd_hash, datetime.utcnow().isoformat() + "Z"),
            )
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe."}), 409

    return jsonify({"mensaje": "Usuario registrado con éxito."}), 201

@app.post("/login")
def login():
    """
    Body JSON: {"usuario": "nombre", "contraseña": "1234"}
    Verifica credenciales y responde 200/401.
    """
    data = request.get_json(silent=True) or {}
    username = data.get("usuario")
    password = data.get("contraseña")

    if not username or not password:
        return jsonify({"error": "Faltan campos: 'usuario' y 'contraseña' son obligatorios."}), 400

    if verify_user(username, password):
        return jsonify({"mensaje": "Login exitoso."}), 200
    else:
        return jsonify({"error": "Credenciales inválidas."}), 401

@app.get("/tareas")
def tareas():
    """
    Requiere Autenticación Básica (Authorization: Basic base64(usuario:contraseña))
    Devuelve una página HTML simple de bienvenida.
    """
    auth_header = request.headers.get("Authorization")
    username, password = parse_basic_auth(auth_header)

    if not username or not password or not verify_user(username, password):
        # Desafío de Basic Auth
        resp = make_response("No autorizado", 401)
        resp.headers["WWW-Authenticate"] = 'Basic realm="PFO2", charset="UTF-8"'
        return resp

    html = f"""
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Bienvenido</title>
        <style>
          body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, 'Noto Sans', 'Apple Color Emoji', 'Segoe UI Emoji'; 
                 margin: 2rem; line-height: 1.5; }}
          .card {{ max-width: 680px; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1.25rem; }}
          h1 {{ margin-top: 0; }}
          code {{ background: #f3f4f6; padding: 0.2rem 0.35rem; border-radius: 6px; }}
        </style>
      </head>
      <body>
        <div class="card">
          <h1>¡Hola, {username}!</h1>
          <p>Tu autenticación fue exitosa.</p>
          <hr>
          <p>Fecha/Hora (UTC): <strong>{datetime.utcnow().isoformat()}Z</strong></p>
        </div>
      </body>
    </html>
    """
    resp = make_response(html, 200)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp

if __name__ == "__main__":
    # Para desarrollo: FLASK_ENV=development python servidor.py
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
