import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def init_db(app):
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        database_url = "sqlite:///blacklist.db"
        print("⚠️  DATABASE_URL no configurada. Usando SQLite por defecto.")
        os.environ["DATABASE_URL"] = database_url
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    return db

def create_tables(app):
    """Crea las tablas solo si no existen."""
    with app.app_context():
        # Verificar si la tabla ya existe
        inspector = db.inspect(db.engine)
        if not inspector.has_table('blacklists'):
            db.create_all()
            print("✅ Tablas creadas correctamente")
        else:
            print("ℹ️  Las tablas ya existen. No se crearon nuevas.")