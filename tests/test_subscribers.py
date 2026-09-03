import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)



def test_create_subscriber():
    response = client.post("/subscribers/", json={
        "name": "Test User",
        "email": "test@example.com",
        "phone": "9876543210",
        "address": "Test Address",
        "latitude": "17.4586",
        "longitude": "78.3737"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_subscriber_not_found():
    response = client.get("/subscribers/999")
    assert response.status_code == 404

def test_full_order_flow():
    # Create a subscriber first
    sub_response = client.post("/subscribers/", json={
        "name": "Order Test User",
        "email": "ordertest@example.com",
        "phone": "9876543211",
        "address": "Kondapur, Hyderabad",
        "latitude": "17.4586",
        "longitude": "78.3737"
    })
    subscriber_id = sub_response.json()["id"]

    # Register and log in to get a token (order creation is protected)
    client.post("/auth/register", json={"username": "testuser1", "password": "testpass123"})
    login_response = client.post("/auth/login", data={"username": "testuser1", "password": "testpass123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create an order
    order_response = client.post("/orders/", json={
        "subscriber_id": subscriber_id,
        "plan_name": "100 Mbps Fiber"
    }, headers=headers)
    assert order_response.status_code == 201
    order_id = order_response.json()["id"]
    assert order_response.json()["status"] == "REQUESTED"

    # Run feasibility check
    feasibility_response = client.post(f"/orders/{order_id}/check-feasibility")
    assert feasibility_response.status_code == 200
    assert feasibility_response.json()["status"] == "FEASIBILITY_CHECKED"


def test_create_order_without_auth_fails():
    response = client.post("/orders/", json={"subscriber_id": 1, "plan_name": "Test Plan"})
    assert response.status_code == 401


def test_register_and_login():
    register_response = client.post("/auth/register", json={
        "username": "newuser",
        "password": "securepass123"
    })
    assert register_response.status_code == 201
    assert "id" in register_response.json()

    login_response = client.post("/auth/login", data={
        "username": "newuser",
        "password": "securepass123"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_login_wrong_password_fails():
    client.post("/auth/register", json={"username": "user2", "password": "correctpass"})
    response = client.post("/auth/login", data={"username": "user2", "password": "wrongpass"})
    assert response.status_code == 401