#!/usr/bin/env python3
"""
SafeSQL-Lab Test Suite
Tests for vulnerable endpoints to ensure they behave as expected
"""

import pytest
import sqlite3
import os
import tempfile
from app import create_app, db
from app.models import User, Product, Comment

@pytest.fixture
def app():
    """Create test application"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        # Seed test data
        seed_test_data()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def seed_test_data():
    """Seed database with test data"""
    # Create test users
    users = [
        User(username='admin', password='admin123', role='admin'),
        User(username='alice', password='password123', role='user'),
        User(username='bob', password='secret456', role='user'),
    ]
    
    for user in users:
        db.session.add(user)
    
    # Create test products
    products = [
        Product(name='Test Product 1', description='Test description 1', price=99.99),
        Product(name='Test Product 2', description='Test description 2', price=199.99),
    ]
    
    for product in products:
        db.session.add(product)
    
    # Create test comments
    comments = [
        Comment(product_id=1, author='alice', content='Test comment 1'),
        Comment(product_id=1, author='bob', content='Test comment 2'),
    ]
    
    for comment in comments:
        db.session.add(comment)
    
    db.session.commit()

class TestVulnerableLogin:
    """Test vulnerable login endpoint"""
    
    def test_valid_login(self, client):
        """Test valid login credentials"""
        response = client.post('/vulnerable/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        assert response.status_code == 200
        assert b'Login successful' in response.data
    
    def test_invalid_login(self, client):
        """Test invalid login credentials"""
        response = client.post('/vulnerable/login', data={
            'username': 'admin',
            'password': 'wrongpassword'
        })
        assert response.status_code == 200
        assert b'Invalid credentials' in response.data
    
    def test_sql_injection_bypass(self, client):
        """Test SQL injection bypass"""
        response = client.post('/vulnerable/login', data={
            'username': "admin'--",
            'password': 'anything'
        })
        assert response.status_code == 200
        assert b'Login successful' in response.data
    
    def test_sql_injection_universal_bypass(self, client):
        """Test universal SQL injection bypass"""
        response = client.post('/vulnerable/login', data={
            'username': "admin' OR '1'='1",
            'password': 'anything'
        })
        assert response.status_code == 200
        assert b'Login successful' in response.data

class TestVulnerableSearch:
    """Test vulnerable search endpoint"""
    
    def test_normal_search(self, client):
        """Test normal search functionality"""
        response = client.get('/vulnerable/search?q=Test')
        assert response.status_code == 200
        assert b'Test Product' in response.data
    
    def test_sql_injection_union(self, client):
        """Test SQL injection with UNION"""
        response = client.get('/vulnerable/search?q=test\' UNION SELECT username,password,role,4 FROM users--')
        assert response.status_code == 200
        # Should return user data instead of product data
        assert b'admin' in response.data or b'alice' in response.data
    
    def test_sql_injection_error(self, client):
        """Test SQL injection that causes error"""
        response = client.get('/vulnerable/search?q=test\'')
        assert response.status_code == 200
        # Should show error message
        assert b'Search error' in response.data

class TestVulnerableItemDetail:
    """Test vulnerable item detail endpoint"""
    
    def test_normal_item_view(self, client):
        """Test normal item detail view"""
        response = client.get('/vulnerable/item?id=1')
        assert response.status_code == 200
        assert b'Test Product 1' in response.data
    
    def test_sql_injection_union(self, client):
        """Test SQL injection with UNION in item detail"""
        response = client.get('/vulnerable/item?id=1 UNION SELECT username,password,role,4,5 FROM users--')
        assert response.status_code == 200
        # Should return user data
        assert b'admin' in response.data or b'alice' in response.data
    
    def test_sql_injection_error(self, client):
        """Test SQL injection that causes error"""
        response = client.get('/vulnerable/item?id=1\'')
        assert response.status_code == 200
        # Should show error message
        assert b'Database error' in response.data

class TestVulnerableComment:
    """Test vulnerable comment endpoint"""
    
    def test_normal_comment(self, client):
        """Test normal comment submission"""
        response = client.post('/vulnerable/comment', data={
            'product_id': '1',
            'author': 'testuser',
            'content': 'This is a test comment'
        })
        assert response.status_code == 200
        assert b'Comment added successfully' in response.data
    
    def test_sql_injection_in_author(self, client):
        """Test SQL injection in author field"""
        response = client.post('/vulnerable/comment', data={
            'product_id': '1',
            'author': "'; INSERT INTO users (username,password,role) VALUES ('hacker','password','admin');--",
            'content': 'Test comment'
        })
        assert response.status_code == 200
        # Should succeed (vulnerable implementation)
        assert b'Comment added successfully' in response.data
    
    def test_sql_injection_in_content(self, client):
        """Test SQL injection in content field"""
        response = client.post('/vulnerable/comment', data={
            'product_id': '1',
            'author': 'testuser',
            'content': "'; DROP TABLE users;--"
        })
        assert response.status_code == 200
        # Should succeed (vulnerable implementation)
        assert b'Comment added successfully' in response.data

class TestVulnerableBooleanBlind:
    """Test vulnerable boolean-based blind injection"""
    
    def test_normal_boolean_query(self, client):
        """Test normal boolean query"""
        response = client.get('/vulnerable/boolean?user_id=1')
        assert response.status_code == 200
        assert b'User found' in response.data
    
    def test_boolean_injection_true(self, client):
        """Test boolean injection with true condition"""
        response = client.get('/vulnerable/boolean?user_id=1 AND 1=1')
        assert response.status_code == 200
        assert b'User found' in response.data
    
    def test_boolean_injection_false(self, client):
        """Test boolean injection with false condition"""
        response = client.get('/vulnerable/boolean?user_id=1 AND 1=2')
        assert response.status_code == 200
        assert b'User not found' in response.data

class TestVulnerableTimeBlind:
    """Test vulnerable time-based blind injection"""
    
    def test_normal_time_query(self, client):
        """Test normal time query"""
        response = client.get('/vulnerable/time?user_id=1')
        assert response.status_code == 200
        assert b'User found' in response.data
    
    def test_time_injection_true(self, client):
        """Test time injection with true condition"""
        response = client.get('/vulnerable/time?user_id=1 AND 1=1')
        assert response.status_code == 200
        assert b'User found' in response.data
    
    def test_time_injection_false(self, client):
        """Test time injection with false condition"""
        response = client.get('/vulnerable/time?user_id=1 AND 1=2')
        assert response.status_code == 200
        assert b'User not found' in response.data

class TestSecureEndpoints:
    """Test secure endpoints to ensure they're not vulnerable"""
    
    def test_secure_login_valid(self, client):
        """Test secure login with valid credentials"""
        response = client.post('/secure/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        assert response.status_code == 200
        assert b'Login successful' in response.data
    
    def test_secure_login_injection_attempt(self, client):
        """Test secure login with injection attempt"""
        response = client.post('/secure/login', data={
            'username': "admin'--",
            'password': 'anything'
        })
        assert response.status_code == 200
        assert b'Invalid credentials' in response.data  # Should fail, not succeed
    
    def test_secure_search_normal(self, client):
        """Test secure search with normal input"""
        response = client.get('/secure/search?q=Test')
        assert response.status_code == 200
        assert b'Test Product' in response.data
    
    def test_secure_search_injection_attempt(self, client):
        """Test secure search with injection attempt"""
        response = client.get('/secure/search?q=test\' UNION SELECT username,password,role,4 FROM users--')
        assert response.status_code == 200
        # Should not return user data
        assert b'admin' not in response.data
        assert b'alice' not in response.data

if __name__ == '__main__':
    pytest.main([__file__])
