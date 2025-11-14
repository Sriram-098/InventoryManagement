"""
Unit tests for database models
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Product, InventoryHistory

# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db_session):
    """Test creating a user"""
    user = User(
        username="testuser",
        email="test@example.com",
        password="hashed_password",
        role="customer"
    )
    db_session.add(user)
    db_session.commit()
    
    # Query the user
    saved_user = db_session.query(User).filter_by(username="testuser").first()
    assert saved_user is not None
    assert saved_user.username == "testuser"
    assert saved_user.email == "test@example.com"
    assert saved_user.role == "customer"
    assert saved_user.is_active == True

def test_user_unique_username(db_session):
    """Test that username must be unique"""
    user1 = User(username="testuser", email="test1@example.com", password="pass1")
    user2 = User(username="testuser", email="test2@example.com", password="pass2")
    
    db_session.add(user1)
    db_session.commit()
    
    db_session.add(user2)
    with pytest.raises(Exception):
        db_session.commit()

def test_create_product(db_session):
    """Test creating a product"""
    product = Product(
        name="Test Product",
        sku="TEST-001",
        description="Test description",
        category="Electronics",
        price=99.99,
        quantity=50,
        min_stock_level=10,
        supplier="Test Supplier"
    )
    db_session.add(product)
    db_session.commit()
    
    saved_product = db_session.query(Product).filter_by(sku="TEST-001").first()
    assert saved_product is not None
    assert saved_product.name == "Test Product"
    assert saved_product.price == 99.99
    assert saved_product.quantity == 50
    assert saved_product.supplier == "Test Supplier"

def test_product_unique_sku(db_session):
    """Test that SKU must be unique"""
    product1 = Product(name="Product 1", sku="SKU-001", price=10.0)
    product2 = Product(name="Product 2", sku="SKU-001", price=20.0)
    
    db_session.add(product1)
    db_session.commit()
    
    db_session.add(product2)
    with pytest.raises(Exception):
        db_session.commit()

def test_product_default_values(db_session):
    """Test product default values"""
    product = Product(
        name="Minimal Product",
        sku="MIN-001",
        price=10.0
    )
    db_session.add(product)
    db_session.commit()
    
    saved_product = db_session.query(Product).filter_by(sku="MIN-001").first()
    assert saved_product.quantity == 0
    assert saved_product.min_stock_level == 10
    assert saved_product.created_at is not None
    assert saved_product.updated_at is not None

def test_create_inventory_history(db_session):
    """Test creating inventory history"""
    # First create a product
    product = Product(name="Test Product", sku="TEST-001", price=10.0)
    db_session.add(product)
    db_session.commit()
    
    # Create history entry
    history = InventoryHistory(
        product_id=product.id,
        action="added",
        quantity_change=50,
        performed_by="admin",
        notes="Initial stock"
    )
    db_session.add(history)
    db_session.commit()
    
    saved_history = db_session.query(InventoryHistory).filter_by(product_id=product.id).first()
    assert saved_history is not None
    assert saved_history.action == "added"
    assert saved_history.quantity_change == 50
    assert saved_history.performed_by == "admin"

def test_multiple_products(db_session):
    """Test creating multiple products"""
    products = [
        Product(name="Product 1", sku="SKU-001", price=10.0, quantity=100),
        Product(name="Product 2", sku="SKU-002", price=20.0, quantity=50),
        Product(name="Product 3", sku="SKU-003", price=30.0, quantity=25),
    ]
    
    for product in products:
        db_session.add(product)
    db_session.commit()
    
    all_products = db_session.query(Product).all()
    assert len(all_products) == 3
    
    # Test total inventory value calculation
    total_value = sum(p.price * p.quantity for p in all_products)
    assert total_value == (10.0 * 100) + (20.0 * 50) + (30.0 * 25)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
