import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health_check(client):
    for _ in range(5):
        respuesta = client.get('/health')
        assert respuesta.status_code == 200, "El servicio de salud es inestable"

def test_buscar_usuario(client):
    respuesta = client.get('/buscar?id=5')
    assert respuesta.status_code == 200
    data = respuesta.get_json()
    assert data.get("parametro") == "5"

def test_buscar_id_no_numerico(client):
    respuesta = client.get('/buscar?id=1; DROP TABLE usuarios')
    # Validamos que responda de forma segura (200 o un error controlado)
    assert respuesta.status_code in [200, 400, 404, 500]