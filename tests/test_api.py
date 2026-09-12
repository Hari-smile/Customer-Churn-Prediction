from flask_api import app

def test_home():
    client =app.test_client()

    response = client.get("/")

    assert response.status_code == 200  

def test_predict_without_api_key():
    client = app.test_client()

    response= client.post("/predict",json={})
    assert response.status_code ==401