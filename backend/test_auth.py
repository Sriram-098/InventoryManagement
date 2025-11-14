"""
Unit tests for authentication module
"""
import pytest
from auth import get_password_hash, verify_password, create_access_token, decode_token

def test_password_hashing():
    """Test password hashing functionality"""
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    # Hash should not equal plain password
    assert hashed != password
    # Hash should be a string
    assert isinstance(hashed, str)
    # Hash should not be empty
    assert len(hashed) > 0

def test_password_verification():
    """Test password verification"""
    password = "secure_password"
    hashed = get_password_hash(password)
    
    # Correct password should verify
    assert verify_password(password, hashed) == True
    # Wrong password should not verify
    assert verify_password("wrong_password", hashed) == False

def test_password_verification_case_sensitive():
    """Test that password verification is case sensitive"""
    password = "MyPassword123"
    hashed = get_password_hash(password)
    
    assert verify_password("MyPassword123", hashed) == True
    assert verify_password("mypassword123", hashed) == False
    assert verify_password("MYPASSWORD123", hashed) == False

def test_create_access_token():
    """Test JWT token creation"""
    data = {"sub": "testuser", "role": "admin"}
    token = create_access_token(data)
    
    # Token should be a string
    assert isinstance(token, str)
    # Token should not be empty
    assert len(token) > 0
    # Token should have 3 parts (header.payload.signature)
    assert len(token.split('.')) == 3

def test_decode_token():
    """Test JWT token decoding"""
    data = {"sub": "testuser", "role": "admin"}
    token = create_access_token(data)
    
    # Decode the token
    decoded = decode_token(token)
    
    # Should contain original data
    assert decoded is not None
    assert decoded["sub"] == "testuser"
    assert decoded["role"] == "admin"
    # Should have expiration
    assert "exp" in decoded

def test_decode_invalid_token():
    """Test decoding invalid token"""
    invalid_token = "invalid.token.here"
    decoded = decode_token(invalid_token)
    
    # Should return None for invalid token
    assert decoded is None

def test_multiple_users_different_hashes():
    """Test that same password generates different hashes (salt)"""
    password = "same_password"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # Hashes should be different due to salt
    assert hash1 != hash2
    # But both should verify correctly
    assert verify_password(password, hash1) == True
    assert verify_password(password, hash2) == True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
