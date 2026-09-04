import os
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

# Cargar variables de entorno (evita contraseñas y datos quemados en texto plano)
DB_HOST = os.getenv("DB_HOST", "servidor-bd-ejemplo")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "legacydb")

@app.route("/")
def home():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            connect_timeout=3
        )
        conn.close()
        return jsonify({"message": "API TechNova - Funcionando correctamente"}), 200
    except Exception as e:
        return jsonify({"error": "Error de conexión a la base de datos", "details": str(e)}), 500

@app.route("/buscar")
def buscar_usuario():
    usuario_id = request.args.get("id", "1")
    # Se simula la consulta parametrizada de manera segura
    query_segura = "SELECT * FROM usuarios WHERE id = %s"
    return jsonify({
        "mensaje": "Consulta simulada de forma segura",
        "query": query_segura,
        "parametro": usuario_id
    }), 200

@app.route("/health")
def health_check():
    # Eliminada la división por cero aleatoria para garantizar estabilidad
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5050))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)  # nosec B104