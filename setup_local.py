#!/usr/bin/env python3
"""
Local Setup Script for SafeSQL-Lab
Alternative setup without Docker for environments with network issues
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'logs', 'instructor']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_database():
    """Setup the database"""
    try:
        from app import create_app, db
        from app.models import User, Product, Comment
        
        app = create_app()
        with app.app_context():
            # Create tables
            db.create_all()
            
            # Check if data already exists
            if User.query.count() == 0:
                # Seed database
                users = [
                    User(username='admin', password='admin123', role='admin'),
                    User(username='alice', password='password123', role='user'),
                    User(username='bob', password='secret456', role='user'),
                    User(username='charlie', password='mypassword', role='user'),
                ]
                
                for user in users:
                    db.session.add(user)
                
                products = [
                    Product(name='Wooden Chair', description='Handcrafted oak chair', price=299.99),
                    Product(name='Dining Table', description='Solid wood dining table', price=899.99),
                    Product(name='Bookshelf', description='5-tier wooden bookshelf', price=199.99),
                    Product(name='Coffee Table', description='Modern wooden coffee table', price=399.99),
                    Product(name='Bed Frame', description='Queen size wooden bed frame', price=1299.99),
                ]
                
                for product in products:
                    db.session.add(product)
                
                comments = [
                    Comment(product_id=1, author='alice', content='Beautiful craftsmanship!'),
                    Comment(product_id=1, author='bob', content='Very sturdy and well-made.'),
                    Comment(product_id=2, author='charlie', content='Perfect for family dinners.'),
                    Comment(product_id=3, author='alice', content='Great storage solution.'),
                ]
                
                for comment in comments:
                    db.session.add(comment)
                
                db.session.commit()
                print("✅ Database created and seeded successfully")
            else:
                print("✅ Database already exists with data")
        
        return True
    except Exception as e:
        print(f"❌ Failed to setup database: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("SafeSQL-Lab Local Setup")
    print("=" * 60)
    print("⚠️  LEGAL WARNING: FOR EDUCATIONAL USE ONLY ⚠️")
    print("This application is designed for authorized security training.")
    print("DO NOT deploy on the public internet.")
    print("=" * 60)
    
    # Create directories
    print("\n1. Creating directories...")
    create_directories()
    
    # Install dependencies
    print("\n2. Installing dependencies...")
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return False
    
    # Setup database
    print("\n3. Setting up database...")
    if not setup_database():
        print("❌ Setup failed at database setup")
        return False
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\nTo start the application:")
    print("  python app.py")
    print("\nTo access the application:")
    print("  http://localhost:5000")
    print("\nTo run tests:")
    print("  python -m pytest tests/")
    print("\nTo reset database:")
    print("  python reset_db.py")
    print("\nRemember: This lab is for educational use only!")
    print("Never deploy on public networks.")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
