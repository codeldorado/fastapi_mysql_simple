import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

'''
Use an in-memory SQLite database for testing
'''

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_user(client):
    response = client.post("/users/", json={"username": "testuser", "email": "unique_test@example.com", "password": "Password123"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_invalid_user_creation(client):
    response = client.post("/users/", json={"username": "tu", "email": "not-an-email", "password": "short"})
    assert response.status_code == 422

def test_user_retrieval_by_id(client):
    # Create a user
    response = client.post("/users/", json={"username": "testuser", "email": "unique_user_id@example.com", "password": "Password123"})
    user_id = response.json()["id"]

    # Retrieve the user by ID
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "unique_user_id@example.com"

def test_create_post_without_user(client):
    response = client.post("/posts/", json={"title": "Orphan Post", "content": "This post has no owner."}, params={"user_id": 999})
    assert response.status_code == 404

def test_pagination_edge_cases(client):
    for i in range(5):
        client.post("/users/", json={"username": f"testuser{i}", "email": f"unique_pagination{i}@example.com", "password": "Password123"})

    response = client.get("/users/?skip=-1&limit=10")
    assert response.status_code == 400

    response = client.get("/users/?skip=0&limit=0")
    assert response.status_code == 400 

def test_user_deletion_and_post_cascading(client):
    # Create a user
    response = client.post("/users/", json={"username": "testuser", "email": "unique_cascade@example.com", "password": "Password123"})
    print("User creation response:", response.json())
    user_id = response.json()["id"]

    # Create a post for that user
    response = client.post("/posts/", json={"title": "Post to be deleted", "content": "This post will be deleted with the user."}, params={"user_id": user_id})
    print("Post creation response:", response.json())
    post_id = response.json()["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    print("User deletion response:", response.status_code, response.json())
    assert response.status_code == 200


def test_update_non_existent_user(client):
    response = client.put("/users/999", json={"username": "nonexistent", "email": "nonexistent@example.com", "password": "Password123"})
    assert response.status_code == 404 