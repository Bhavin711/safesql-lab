#!/usr/bin/env python3
"""
Virtual Environment Setup Script for SafeSQL-Lab
For systems with externally managed Python environments (like Kali Linux)
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def create_virtual_environment():
    """Create a virtual environment"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_venv_python():
    """Get the path to the virtual environment Python"""
    if os.name == 'nt':  # Windows
        return Path("venv/Scripts/python.exe")
    else:  # Unix-like
        return Path("venv/bin/python")

def get_venv_pip():
    """Get the path to the virtual environment pip"""
    if os.name == 'nt':  # Windows
        return Path("venv/Scripts/pip.exe")
    else:  # Unix-like
        return Path("venv/bin/pip")

def install_dependencies():
    """Install Python dependencies in virtual environment"""
    try:
        pip_path = get_venv_pip()
        subprocess.check_call([str(pip_path), 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully in virtual environment")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'logs', 'instructor']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_database():
    """Setup the database using virtual environment Python"""
    try:
        python_path = get_venv_python()
        
        # Import and setup database
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", "app/__init__.py")
        app_module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, ".")
        spec.loader.exec_module(app_module)
        
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

def create_start_script():
    """Create a start script for the virtual environment"""
    python_path = get_venv_python()
    
    if os.name == 'nt':  # Windows
        start_script = "start_safesql.bat"
        content = f"""@echo off
echo Starting SafeSQL-Lab...
{python_path} app.py
pause
"""
    else:  # Unix-like
        start_script = "start_safesql.sh"
        content = f"""#!/bin/bash
echo "Starting SafeSQL-Lab..."
{python_path} app.py
"""
    
    with open(start_script, 'w') as f:
        f.write(content)
    
    if os.name != 'nt':
        os.chmod(start_script, 0o755)
    
    print(f"✅ Created start script: {start_script}")

def main():
    """Main setup function"""
    print("=" * 60)
    print("SafeSQL-Lab Virtual Environment Setup")
    print("=" * 60)
    print("⚠️  LEGAL WARNING: FOR EDUCATIONAL USE ONLY ⚠️")
    print("This application is designed for authorized security training.")
    print("DO NOT deploy on the public internet.")
    print("=" * 60)
    
    # Create directories
    print("\n1. Creating directories...")
    create_directories()
    
    # Create virtual environment
    print("\n2. Creating virtual environment...")
    if not create_virtual_environment():
        print("❌ Setup failed at virtual environment creation")
        return False
    
    # Install dependencies
    print("\n3. Installing dependencies...")
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return False
    
    # Setup database
    print("\n4. Setting up database...")
    if not setup_database():
        print("❌ Setup failed at database setup")
        return False
    
    # Create start script
    print("\n5. Creating start script...")
    create_start_script()
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\nTo start the application:")
    if os.name == 'nt':
        print("  start_safesql.bat")
    else:
        print("  ./start_safesql.sh")
        print("  # OR")
        print("  venv/bin/python app.py")
    print("\nTo access the application:")
    print("  http://localhost:5000")
    print("\nTo run tests:")
    print("  venv/bin/python -m pytest tests/")
    print("\nTo reset database:")
    print("  venv/bin/python reset_db.py")
    print("\nRemember: This lab is for educational use only!")
    print("Never deploy on public networks.")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
