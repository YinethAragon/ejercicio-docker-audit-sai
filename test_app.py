from app import app

def test_health_check():
    cliente = app.test_client()
    for _ in range(5):
        respuesta = cliente.get('/health')
        assert respuesta.status_code == 200, "El servicio de salud es inestable"

def test_buscar_usuario():
    cliente = app.test_client()
    respuesta = cliente.get('/buscar?id=5')
    assert respuesta.status_code == 200
    assert respuesta.get_json()["parametro"] == "5"