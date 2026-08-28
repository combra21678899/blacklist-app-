import pytest
import os
from flask import Flask, jsonify
from src.middleware.auth_middleware import require_bearer_token


def test_require_bearer_token_without_token():
    """Prueba que falla sin token"""
    app = Flask(__name__)
    
    @app.route('/test')
    @require_bearer_token
    def test():
        return jsonify({"message": "ok"})
    
    with app.test_client() as client:
        response = client.get('/test')
        assert response.status_code == 401
        assert "Missing Authorization header" in response.json["message"]


def test_require_bearer_token_invalid_format():
    """Prueba que falla con formato inválido"""
    app = Flask(__name__)
    
    @app.route('/test')
    @require_bearer_token
    def test():
        return jsonify({"message": "ok"})
    
    with app.test_client() as client:
        response = client.get('/test', headers={"Authorization": "Invalid token"})
        assert response.status_code == 401
        assert "Invalid Authorization header format" in response.json["message"]


def test_require_bearer_token_invalid_token():
    """Prueba que falla con token inválido"""
    os.environ['BEARER_TOKEN'] = 'valid-token'
    app = Flask(__name__)
    
    @app.route('/test')
    @require_bearer_token
    def test():
        return jsonify({"message": "ok"})
    
    with app.test_client() as client:
        response = client.get('/test', headers={"Authorization": "Bearer invalid-token"})
        assert response.status_code == 401
        assert "Invalid token" in response.json["message"]