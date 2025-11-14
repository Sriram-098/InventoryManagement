"""
Unit tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
from models import User, Product
from auth import get_password_hash

# Test database
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create test client"""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(client):
    """Create a test user"""
    db = TestSessionLocal()
    user = User(
        username="testuser",
        email="test@example.com",
        password=get_password_hash("testpass123"),
        role="customer"
    )
    db.add(user)
    db.commit()
    db.close()
    return {"username": "testuser", "password": "testpass123"}

@pytest.fixture
def test_admin(client):
    """Create a test admin user"""
    db = TestSessionLocal()
    admin = User(
        username="testadmin",
        email="admin@example.com",
        password=get_password_hash("adminpass123"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.close()
    return {"username": "testadmin", "password": "adminpass123"}

@pytest.fixture
def admin_token(client, test_admin):
    """Get admin authentication token"""
    response = client.post("/api/auth/login", json=test_admin)
    return response.json()["access_token"]

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_register_user(client):
    """Test user registration"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "role": "customer"
    }
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
    assert response.json()["role"] == "customer"

def test_register_duplicate_username(client, test_user):
    """Test registering with duplicate username"""
    user_data = {
        "username": "testuser",
        "email": "another@example.com",
        "password": "password123",
        "role": "customer"
    }
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400

def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post("/api/auth/login", json=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "user" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    response = client.post("/api/auth/login", json={
        "username": test_user["username"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_products_unauthorized(client):
    """Test getting products without authentication"""
    response = client.get("/api/products/")
    assert response.status_code == 403

def test_create_product_as_admin(client, admin_token):
    """Test creating product as admin"""
    product_data = {
        "name": "Test Product",
        "sku": "TEST-001",
        "description": "Test description",
        "category": "Electronics",
        "price": 99.99,
        "quantity": 50,
        "min_stock_level": 10,
        "supplier": "Test Supplier"
    }
    response = client.post(
        "/api/products/",
        json=product_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    assert response.json()["sku"] == "TEST-001"

def test_get_products_as_admin(client, admin_token):
    """Test getting all products as admin"""
    # Create a product first
    product_data = {
        "name": "Test Product",
        "sku": "TEST-001",
        "price": 99.99,
        "quantity": 50
    }
    client.post(
        "/api/products/",
        json=product_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Get all products
    response = client.get(
        "/api/products/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_product_as_admin(client, admin_token):
    """Test updating product as admin"""
    # Create product
    product_data = {
        "name": "Original Name",
        "sku": "TEST-001",
        "price": 50.0,
        "quantity": 100
    }
    create_response = client.post(
        "/api/products/",
        json=product_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product_id = create_response.json()["id"]
    
    # Update product
    update_data = {"name": "Updated Name", "price": 75.0}
    response = client.put(
        f"/api/products/{product_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["price"] == 75.0

def test_delete_product_as_admin(client, admin_token):
    """Test deleting product as admin"""
    # Create product
    product_data = {
        "name": "To Delete",
        "sku": "DEL-001",
        "price": 10.0
    }
    create_response = client.post(
        "/api/products/",
        json=product_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product_id = create_response.json()["id"]
    
    # Delete product
    response = client.delete(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(
        f"/api/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_response.status_code == 404

def test_get_stats_as_admin(client, admin_token):
    """Test getting statistics as admin"""
    response = client.get(
        "/api/reports/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert "total_products" in response.json()
    assert "total_value" in response.json()
    assert "low_stock_items" in response.json()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
