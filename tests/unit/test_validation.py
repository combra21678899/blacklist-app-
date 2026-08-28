import pytest
from src.utils.validation import validate_uuid, get_client_ip
from src.models.errors import BadRequestError


class TestValidation:
    
    def test_validate_uuid_valid(self):
        """Prueba validar UUID válido"""
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        result = validate_uuid(valid_uuid)
        assert result == True
    
    def test_validate_uuid_invalid(self):
        """Prueba validar UUID inválido"""
        invalid_uuid = "uuid-invalido"
        with pytest.raises(BadRequestError) as exc_info:
            validate_uuid(invalid_uuid)
        assert "Invalid UUID format" in str(exc_info.value)
    
    def test_get_client_ip_with_forwarded_header(self):
        """Prueba obtener IP con header X-Forwarded-For"""
        # Crear un request mock con header
        class MockRequest:
            headers = {"X-Forwarded-For": "192.168.1.1, 10.0.0.1"}
            remote_addr = "127.0.0.1"
        
        result = get_client_ip(MockRequest())
        assert result == "192.168.1.1"
    
    def test_get_client_ip_without_forwarded_header(self):
        """Prueba obtener IP sin header X-Forwarded-For"""
        class MockRequest:
            headers = {}
            remote_addr = "192.168.1.100"
        
        result = get_client_ip(MockRequest())
        assert result == "192.168.1.100"
    
    def test_get_client_ip_with_unknown_remote_addr(self):
        """Prueba obtener IP cuando remote_addr es None"""
        class MockRequest:
            headers = {}
            remote_addr = None
        
        result = get_client_ip(MockRequest())
        assert result == "unknown"