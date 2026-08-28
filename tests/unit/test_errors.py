import pytest
from src.models.errors import BadRequestError, NotFoundError, ConflictError, UnauthorizedError


class TestErrors:
    
    def test_bad_request_error(self):
        """Prueba BadRequestError"""
        error = BadRequestError("Mensaje de error")
        assert str(error) == "Mensaje de error"
        assert error.message == "Mensaje de error"
    
    def test_not_found_error(self):
        """Prueba NotFoundError"""
        error = NotFoundError("No encontrado")
        assert str(error) == "No encontrado"
        assert error.message == "No encontrado"
    
    def test_conflict_error(self):
        """Prueba ConflictError"""
        error = ConflictError("Conflicto detectado")
        assert str(error) == "Conflicto detectado"
        assert error.message == "Conflicto detectado"
    
    def test_unauthorized_error(self):
        """Prueba UnauthorizedError"""
        error = UnauthorizedError("No autorizado")
        assert str(error) == "No autorizado"
        assert error.message == "No autorizado"