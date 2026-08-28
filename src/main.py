import os
import sys
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno
load_dotenv()

# Configurar DATABASE_URL si no existe
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///blacklist.db'

from src.db.database import init_db, create_tables, db
from src.routes.blacklist_router import blacklist_bp
from src.models.errors import BadRequestError, NotFoundError, ConflictError, UnauthorizedError

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar CORS
CORS(app)

# Inicializar base de datos
init_db(app)

# Crear tablas
with app.app_context():
    create_tables(app)

# Registrar blueprints
app.register_blueprint(blacklist_bp)

# Manejadores de errores
@app.errorhandler(BadRequestError)
def handle_bad_request(e):
    return jsonify({"error": "Bad Request", "message": str(e)}), 400

@app.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({"error": "Not Found", "message": str(e)}), 404

@app.errorhandler(ConflictError)
def handle_conflict(e):
    return jsonify({"error": "Conflict", "message": str(e)}), 409

@app.errorhandler(UnauthorizedError)
def handle_unauthorized(e):
    return jsonify({"error": "Unauthorized", "message": str(e)}), 401

@app.errorhandler(Exception)
def handle_generic_error(e):
    print(f"❌ Error: {e}")
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

# Ruta de health check
@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("🚀 Iniciando servidor en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)