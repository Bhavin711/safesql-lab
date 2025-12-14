#!/usr/bin/env python3
"""
Database Reset Script for SafeSQL-Lab
Resets the database to its initial seeded state
"""

import os
import sys
from app import create_app, db
from app.models import User, Product, Comment, ExerciseLog

def reset_database():
    """Reset database to initial state"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Seed database with initial data
        seed_database()
        
        print("Database reset successfully!")
        print("Initial data has been restored.")

def seed_database():
    """Seed database with initial data"""
    # Create users
    users = [
        User(username='admin', password='admin123', role='admin'),
        User(username='alice', password='password123', role='user'),
        User(username='bob', password='secret456', role='user'),
        User(username='charlie', password='mypassword', role='user'),
    ]
    
    for user in users:
        db.session.add(user)
    
    # Create products
    products = [
        Product(name='Wooden Chair', description='Handcrafted oak chair', price=299.99),
        Product(name='Dining Table', description='Solid wood dining table', price=899.99),
        Product(name='Bookshelf', description='5-tier wooden bookshelf', price=199.99),
        Product(name='Coffee Table', description='Modern wooden coffee table', price=399.99),
        Product(name='Bed Frame', description='Queen size wooden bed frame', price=1299.99),
    ]
    
    for product in products:
        db.session.add(product)
    
    # Create comments
    comments = [
        Comment(product_id=1, author='alice', content='Beautiful craftsmanship!'),
        Comment(product_id=1, author='bob', content='Very sturdy and well-made.'),
        Comment(product_id=2, author='charlie', content='Perfect for family dinners.'),
        Comment(product_id=3, author='alice', content='Great storage solution.'),
    ]
    
    for comment in comments:
        db.session.add(comment)
    
    db.session.commit()
    print("Database seeded with initial data!")

if __name__ == '__main__':
    reset_database()
