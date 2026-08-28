import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask app.
    """
    # Get database URL from environment variables
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        # Si no está configurada, usar SQLite por defecto para desarrollo
        database_url = "sqlite:///blacklist.db"
        print("⚠️  DATABASE_URL no configurada. Usando SQLite por defecto.")
        os.environ["DATABASE_URL"] = database_url
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize the app with the database
    db.init_app(app)
    
    return db

def create_tables(app):
    """
    Create all tables in the database.
    """
    with app.app_context():
        db.create_all()
        print("✅ Tablas creadas correctamente")