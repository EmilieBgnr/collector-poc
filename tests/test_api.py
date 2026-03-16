from fastapi.testclient import TestClient
from app.main import app, ARTICLES_DB, MEDIA_DIR
import os
import shutil

client = TestClient(app)

def setup_function():
    ARTICLES_DB.clear()
    if os.path.exists(MEDIA_DIR):
        shutil.rmtree(MEDIA_DIR)
    os.makedirs(MEDIA_DIR, exist_ok=True)

def test_create_article_ok():
    files = {
        "image": ("test.png", b"fakeimage", "image/png")
    }
    data = {
        "title": "Sabre laser",
        "description": "Sabre original",
        "price": "199.99",
        "category": "Star Wars"
    }

    response = client.post("/articles", data=data, files=files)
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Sabre laser"
    assert body["status"] == "PENDING_VALIDATION"

def test_get_article_not_found():
    response = client.get("/articles/unknown")
    assert response.status_code == 404
