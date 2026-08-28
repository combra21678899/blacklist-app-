import pytest
from unittest.mock import Mock, patch
from src.services.blacklist_service import BlacklistService
from src.models.errors import ConflictError


class TestBlacklistService:
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_add_to_blacklist_success(self, mock_repo):
        """Prueba que agrega un email exitosamente"""
        # Configurar mock del repositorio
        mock_instance = Mock()
        mock_instance.create.return_value = Mock(
            id="123e4567-e89b-12d3-a456-426614174000",
            email="test@example.com",
            created_at=Mock(isoformat=lambda: "2026-01-01T00:00:00")
        )
        mock_repo.return_value = mock_instance
        
        # Crear servicio y ejecutar
        service = BlacklistService()
        result = service.add_to_blacklist(
            email="test@example.com",
            app_uuid="123e4567-e89b-12d3-a456-426614174000",
            blocked_reason="Spam detectado",
            ip_address="127.0.0.1"
        )
        
        # Verificar resultado
        assert result["email"] == "test@example.com"
        assert "added to blacklist" in result["message"]
        assert result["id"] == "123e4567-e89b-12d3-a456-426614174000"
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_check_blacklist_found(self, mock_repo):
        """Prueba que verifica un email que SÍ está en la lista negra"""
        mock_instance = Mock()
        mock_instance.get_by_email.return_value = Mock(
            blocked_reason="Spam detectado"
        )
        mock_repo.return_value = mock_instance
        
        service = BlacklistService()
        result = service.check_blacklist("test@example.com")
        
        assert result["is_blacklisted"] == True
        assert result["email"] == "test@example.com"
        assert result["blocked_reason"] == "Spam detectado"
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_check_blacklist_not_found(self, mock_repo):
        """Prueba que verifica un email que NO está en la lista negra"""
        mock_instance = Mock()
        mock_instance.get_by_email.return_value = None
        mock_repo.return_value = mock_instance
        
        service = BlacklistService()
        result = service.check_blacklist("nonexistent@example.com")
        
        assert result["is_blacklisted"] == False
        assert result["email"] == "nonexistent@example.com"
        assert result["blocked_reason"] is None

        # Agregar al final del archivo test_blacklist_service.py
