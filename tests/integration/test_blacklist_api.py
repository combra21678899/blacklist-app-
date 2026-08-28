import pytest
import os
from src.main import app
from src.db.database import db, create_tables


@pytest.fixture
def client():
    """Fixture para el cliente de prueba con base de datos limpia"""
    # Configurar variables de entorno para pruebas
    os.environ['BEARER_TOKEN'] = 'dev-token-12345'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Crear tablas en la base de datos en memoria
    with app.app_context():
        create_tables(app)
    
    with app.test_client() as client:
        yield client
    
    # Limpiar después de las pruebas
    with app.app_context():
        db.drop_all()


class TestBlacklistAPI:
    
    def test_ping_endpoint(self, client):
        """Prueba el endpoint de salud /ping"""
        response = client.get('/blacklists/ping')
        assert response.status_code == 200
        assert response.json == {"message": "pong"}
    
    def test_health_endpoint(self, client):
        """Prueba el endpoint de salud /health"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json == {"status": "healthy"}
    
    def test_create_blacklist_success(self, client):
        """Prueba crear un email en lista negra exitosamente"""
        data = {
            "email": "test@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spam detectado"
        }
        response = client.post(
            '/blacklists',
            json=data,
            headers={"Authorization": "Bearer dev-token-12345"}
        )
        assert response.status_code == 201
        assert response.json["email"] == "test@example.com"
    
    def test_create_blacklist_invalid_email(self, client):
        """Prueba crear con email inválido"""
        data = {
            "email": "email-invalido",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spam"
        }
        response = client.post(
            '/blacklists',
            json=data,
            headers={"Authorization": "Bearer dev-token-12345"}
        )
        assert response.status_code == 400
    
    def test_create_blacklist_invalid_uuid(self, client):
        """Prueba crear con UUID inválido"""
        data = {
            "email": "test@example.com",
            "app_uuid": "uuid-invalido",
            "blocked_reason": "Spam"
        }
        response = client.post(
            '/blacklists',
            json=data,
            headers={"Authorization": "Bearer dev-token-12345"}
        )
        assert response.status_code == 400
    
    def test_create_blacklist_duplicate_email(self, client):
        """Prueba crear un email duplicado"""
        data = {
            "email": "duplicate@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spam"
        }
        # Crear primero
        client.post(
            '/blacklists',
            json=data,
            headers={"Authorization": "Bearer dev-token-12345"}
        )
        # Intentar crear duplicado
        response = client.post(
            '/blacklists',
            json=data,
            headers={"Authorization": "Bearer dev-token-12345"}
        )
        assert response.status_code == 409
    
    def test_check_blacklist_found(self, client):
        """Prueba consultar un email que SÍ está en la lista negra"""
        # Primero creamos uno
        data = {
            "email": "check@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spam"
        }
        client.post(
            '/blacklists',
            json=data,
            headers={"Authorization": "Bearer dev-token-12345"}
        )
        
        # Luego lo consultamos
        response = client.get(
            '/blacklists/check@example.com',
            headers={"Authorization": "Bearer dev-token-12345"}
        )
        assert response.status_code == 200
        assert response.json["is_blacklisted"] == True
        assert response.json["email"] == "check@example.com"
    
    def test_check_blacklist_not_found(self, client):
        """Prueba consultar un email que NO está en la lista negra"""
        response = client.get(
            '/blacklists/noexiste@example.com',
            headers={"Authorization": "Bearer dev-token-12345"}
        )
        assert response.status_code == 200
        assert response.json["is_blacklisted"] == False
        assert response.json["email"] == "noexiste@example.com"
    
    def test_create_blacklist_unauthorized(self, client):
        """Prueba crear sin token de autenticación"""
        data = {
            "email": "test@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spam"
        }
        response = client.post('/blacklists', json=data)
        assert response.status_code == 401