from flask import Flask, request, jsonify
import sqlite3
import bcrypt

app = Flask(__name__)

# --------------------------
# Función auxiliar: conexión
# --------------------------
def get_db_connection():
    conn = sqlite3.connect("tareas.db")
    conn.row_factory = sqlite3.Row
    return conn

# --------------------------
# Endpoint: Registro
# --------------------------
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")

    if not usuario or not password:
        return jsonify({"error": "Faltan datos"}), 400

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (usuario, hashed))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Usuario ya existe"}), 400
    finally:
        conn.close()

    return jsonify({"mensaje": f"Usuario {usuario} registrado correctamente"}), 201

# --------------------------
# Endpoint: Login
# --------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")

    if not usuario or not password:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password, id FROM usuarios WHERE username = ?", (usuario,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    hashed = row[0]
    user_id = row[1]

    if bcrypt.checkpw(password.encode("utf-8"), hashed):
        return jsonify({"mensaje": f"Bienvenido {usuario}", "user_id": user_id}), 200
    else:
        return jsonify({"error": "Contraseña incorrecta"}), 401

# --------------------------
# Endpoint: Crear tarea
# --------------------------
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    data = request.get_json()
    descripcion = data.get("descripcion")
    usuario_id = data.get("user_id")  # por ahora pasamos el id en el body

    if not descripcion or not usuario_id:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tareas (descripcion, usuario_id) VALUES (?, ?)", (descripcion, usuario_id))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Tarea creada correctamente"}), 201

# --------------------------
# Endpoint: Listar tareas
# --------------------------
@app.route('/tareas', methods=['GET'])
def listar_tareas():
    usuario_id = request.args.get("user_id")  # por ahora pasamos el id como parámetro

    if not usuario_id:
        return jsonify({"error": "Falta el user_id"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, descripcion, estado FROM tareas WHERE usuario_id = ?", (usuario_id,))
    tareas = cur.fetchall()
    conn.close()

    lista = [{"id": t["id"], "descripcion": t["descripcion"], "estado": t["estado"]} for t in tareas]

    return jsonify({"tareas": lista}), 200

# --------------------------
# Ejecutar servidor
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
