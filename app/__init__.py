from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'lab-training-key-change-in-production'
    
    # Get absolute path for database
    db_path = os.path.abspath('data/lab.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{db_path}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Security: Only bind to localhost by default
    app.config['HOST'] = os.getenv('HOST', '127.0.0.1')
    app.config['PORT'] = int(os.getenv('PORT', 5000))
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.vulnerable import vulnerable_bp
    from app.routes.secure import secure_bp
    from app.routes.exercises import exercises_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(vulnerable_bp, url_prefix='/vulnerable')
    app.register_blueprint(secure_bp, url_prefix='/secure')
    app.register_blueprint(exercises_bp, url_prefix='/exercises')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Seed database if empty
        from app.models import User, Product, Comment
        if User.query.count() == 0:
            seed_database()
    
    return app

def seed_database():
    """Seed the database with initial data"""
    from app.models import User, Product, Comment
    
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
    print("Database seeded successfully!")
