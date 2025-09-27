
import pytest
from fastapi.testclient import TestClient

class TestMudanzasAPI:
    """
    Tests específicos para Mudanzas - FICHA 3147246
    """

    def test_create_traslado_success(self, client, sample_traslado_data, auth_headers):
        """Test de creación exitosa de traslado en Mudanzas"""
        response = client.post(
            "/moving_traslados/",
            json=sample_traslado_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()

        # Validaciones específicas de Mudanzas
        assert data["origen"] == sample_traslado_data["origen"]
        assert data["destino"] == sample_traslado_data["destino"]
        assert data["cliente"] == sample_traslado_data["cliente"]

    def test_get_traslado_not_found(self, client, auth_headers):
        """Test de traslado no encontrado en Mudanzas"""
        response = client.get("/moving_traslados/999", headers=auth_headers)

        assert response.status_code == 404
        assert "traslado no encontrado" in response.json()["detail"]

    def test_traslado_validation_error(self, client, auth_headers):
        """Test de validación específica para Mudanzas"""
        # Datos inválidos específicos de Mudanzas
        invalid_data = {
            "origen": "",  # Campo requerido vacío
            "destino": "Medellín",
            "cliente": ""  # Cliente vacío, inválido
        }

        response = client.post(
            "/moving_traslados/",
            json=invalid_data,
            headers=auth_headers
        )

        assert response.status_code == 422
        errors = response.json()["detail"]

        # Validar errores específicos
        assert any("origen" in str(error) for error in errors)
        assert any("cliente" in str(error) for error in errors)

