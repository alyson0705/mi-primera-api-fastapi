
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base

# Base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_moving.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# FIXTURE ESPECÍFICA PARA TU DOMINIO (Mudanzas - traslado)
@pytest.fixture
def sample_traslado_data():
    """
    Datos de ejemplo específicos para el dominio Mudanzas
    """
    return {
        "origen": "Bogotá",
        "destino": "Medellín",
        "fecha": "2025-10-01",
        "cliente": "Juan Pérez",
        "telefono": "3001234567",
        "tipo_servicio": "residencial",
        "observaciones": "Traslado de muebles y enseres"
    }

@pytest.fixture
def auth_headers(client):
    """Headers de autenticación para tests"""
    # Crear usuario de prueba específico para Mudanzas
    response = client.post("/auth/register", json={
        "username": "admin_moving",
        "password": "test123",
        "role": "admin"  # Rol específico de tu dominio
    })

    login_response = client.post("/auth/login", data={
        "username": "admin_moving",
        "password": "test123"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

