from flask import Blueprint, render_template, request, jsonify, session
from app import db
from app.models import ExerciseLog
import logging

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page with legal warnings and project overview"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Exercise dashboard showing available exercises"""
    exercises = [
        {
            'id': 'login_basic',
            'name': 'Basic Login Injection',
            'difficulty': 'Easy',
            'description': 'Learn basic SQL injection through login form',
            'endpoint': '/vulnerable/login'
        },
        {
            'id': 'search_basic',
            'name': 'Product Search Injection',
            'difficulty': 'Easy',
            'description': 'Inject SQL through search parameters',
            'endpoint': '/vulnerable/search'
        },
        {
            'id': 'item_detail',
            'name': 'Item Detail Injection',
            'difficulty': 'Medium',
            'description': 'Numeric parameter injection',
            'endpoint': '/vulnerable/item'
        },
        {
            'id': 'comment_form',
            'name': 'Comment Form Injection',
            'difficulty': 'Medium',
            'description': 'Injection through comment submission',
            'endpoint': '/vulnerable/comment'
        },
        {
            'id': 'boolean_blind',
            'name': 'Boolean-based Blind Injection',
            'difficulty': 'Hard',
            'description': 'Advanced blind injection techniques',
            'endpoint': '/vulnerable/boolean'
        },
        {
            'id': 'time_blind',
            'name': 'Time-based Blind Injection',
            'difficulty': 'Hard',
            'description': 'Time-based blind injection',
            'endpoint': '/vulnerable/time'
        }
    ]
    
    return render_template('dashboard.html', exercises=exercises)

@main_bp.route('/legal-warning')
def legal_warning():
    """Legal warning page that must be acknowledged"""
    return render_template('legal_warning.html')

@main_bp.route('/acknowledge-warning', methods=['POST'])
def acknowledge_warning():
    """Mark that user has acknowledged legal warning"""
    session['legal_acknowledged'] = True
    return jsonify({'status': 'acknowledged'})

@main_bp.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    return jsonify({'status': 'healthy', 'service': 'safesql-lab'})

@main_bp.route('/about')
def about():
    """About page with project information"""
    return render_template('about.html')

@main_bp.route('/secure-examples')
def secure_examples():
    """Show secure implementations"""
    return render_template('secure_examples.html')

@main_bp.before_request
def check_legal_acknowledgment():
    """Ensure user has acknowledged legal warning before accessing exercises"""
    if request.endpoint and request.endpoint.startswith('vulnerable.'):
        if not session.get('legal_acknowledged'):
            return render_template('legal_warning.html'), 403
