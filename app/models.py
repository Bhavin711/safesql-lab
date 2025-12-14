from app import db
from datetime import datetime

class User(db.Model):
    """User model for authentication exercises"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    """Product model for search and display exercises"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Comment(db.Model):
    """Comment model for injection exercises"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    product = db.relationship('Product', backref=db.backref('comments', lazy=True))
    
    def __repr__(self):
        return f'<Comment by {self.author}>'

class ExerciseLog(db.Model):
    """Log model for tracking exercise attempts"""
    __tablename__ = 'exercise_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(100), nullable=False)
    user_input = db.Column(db.Text)
    success = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    
    def __repr__(self):
        return f'<ExerciseLog {self.exercise_name} - {"Success" if self.success else "Failed"}>'
