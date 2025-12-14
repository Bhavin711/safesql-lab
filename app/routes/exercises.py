from flask import Blueprint, render_template, request, jsonify, session
from app import db
from app.models import ExerciseLog
import json

exercises_bp = Blueprint('exercises', __name__)

@exercises_bp.route('/<exercise_id>')
def exercise_detail(exercise_id):
    """Show detailed exercise information and instructions"""
    
    exercises = {
        'login_basic': {
            'name': 'Basic Login Injection',
            'difficulty': 'Easy',
            'description': 'Learn basic SQL injection through login form',
            'vulnerable_endpoint': '/vulnerable/login',
            'secure_endpoint': '/secure/login',
            'learning_objectives': [
                'Understand how string concatenation in SQL creates vulnerabilities',
                'Learn to identify login bypass techniques',
                'Practice with basic SQL injection payloads',
                'Compare vulnerable vs secure implementations'
            ],
            'hints': {
                'low': 'Try using single quotes in the username field',
                'medium': 'Look for ways to comment out the password check',
                'high': 'Use payloads like: admin\'-- or admin\' OR \'1\'=\'1'
            },
            'what_to_look_for': [
                'Input reflected in SQL query',
                'Error messages revealing database structure',
                'Unexpected login success',
                'Ability to bypass authentication'
            ],
            'verification_criteria': 'Successfully bypass login with SQL injection'
        },
        'search_basic': {
            'name': 'Product Search Injection',
            'difficulty': 'Easy',
            'description': 'Inject SQL through search parameters',
            'vulnerable_endpoint': '/vulnerable/search',
            'secure_endpoint': '/secure/search',
            'learning_objectives': [
                'Understand parameter injection vulnerabilities',
                'Learn to extract data through search functions',
                'Practice UNION-based injection techniques',
                'Identify information disclosure through errors'
            ],
            'hints': {
                'low': 'Try special characters in the search box',
                'medium': 'Look for ways to extract table structure',
                'high': 'Use UNION SELECT to extract data from other tables'
            },
            'what_to_look_for': [
                'Search results revealing database structure',
                'Error messages with table/column names',
                'Ability to extract data from other tables',
                'Unexpected search results'
            ],
            'verification_criteria': 'Successfully extract user data through search injection'
        },
        'item_detail': {
            'name': 'Item Detail Injection',
            'difficulty': 'Medium',
            'description': 'Numeric parameter injection',
            'vulnerable_endpoint': '/vulnerable/item',
            'secure_endpoint': '/secure/item',
            'learning_objectives': [
                'Understand numeric parameter vulnerabilities',
                'Learn stacked query injection techniques',
                'Practice data extraction through ID parameters',
                'Identify blind injection opportunities'
            ],
            'hints': {
                'low': 'Try modifying the ID parameter in the URL',
                'medium': 'Look for ways to execute multiple SQL statements',
                'high': 'Use stacked queries to extract or modify data'
            },
            'what_to_look_for': [
                'Ability to modify ID parameter behavior',
                'Error messages revealing database structure',
                'Unexpected data returned',
                'Ability to execute multiple statements'
            ],
            'verification_criteria': 'Successfully extract sensitive data through ID parameter'
        },
        'comment_form': {
            'name': 'Comment Form Injection',
            'difficulty': 'Medium',
            'description': 'Injection through comment submission',
            'vulnerable_endpoint': '/vulnerable/comment',
            'secure_endpoint': '/secure/comment',
            'learning_objectives': [
                'Understand form-based injection vulnerabilities',
                'Learn to inject through multiple parameters',
                'Practice data manipulation techniques',
                'Identify stored procedure vulnerabilities'
            ],
            'hints': {
                'low': 'Try special characters in the comment fields',
                'medium': 'Look for ways to modify the database structure',
                'high': 'Use injection to create or modify user accounts'
            },
            'what_to_look_for': [
                'Ability to inject through form fields',
                'Error messages revealing database structure',
                'Unexpected database modifications',
                'Ability to create or modify records'
            ],
            'verification_criteria': 'Successfully modify database through comment injection'
        },
        'boolean_blind': {
            'name': 'Boolean-based Blind Injection',
            'difficulty': 'Hard',
            'description': 'Advanced blind injection techniques',
            'vulnerable_endpoint': '/vulnerable/boolean',
            'secure_endpoint': '/secure/boolean',
            'learning_objectives': [
                'Understand blind SQL injection concepts',
                'Learn boolean-based inference techniques',
                'Practice data extraction without direct output',
                'Master advanced injection methodologies'
            ],
            'hints': {
                'low': 'Look for different responses based on true/false conditions',
                'medium': 'Try to infer data by testing boolean conditions',
                'high': 'Use binary search techniques to extract data character by character'
            },
            'what_to_look_for': [
                'Different responses for true vs false conditions',
                'Ability to infer data through response differences',
                'Patterns in response behavior',
                'Opportunities for automated data extraction'
            ],
            'verification_criteria': 'Successfully extract sensitive data using boolean-based blind injection'
        },
        'time_blind': {
            'name': 'Time-based Blind Injection',
            'difficulty': 'Hard',
            'description': 'Time-based blind injection',
            'vulnerable_endpoint': '/vulnerable/time',
            'secure_endpoint': '/secure/time',
            'learning_objectives': [
                'Understand time-based blind injection',
                'Learn to use timing for data inference',
                'Practice advanced injection techniques',
                'Master automated exploitation methods'
            ],
            'hints': {
                'low': 'Look for different response times based on conditions',
                'medium': 'Try to use timing functions to infer data',
                'high': 'Use SLEEP() or similar functions to create timing differences'
            },
            'what_to_look_for': [
                'Different response times for different conditions',
                'Ability to infer data through timing analysis',
                'Patterns in response timing',
                'Opportunities for automated timing-based extraction'
            ],
            'verification_criteria': 'Successfully extract data using time-based blind injection'
        }
    }
    
    exercise = exercises.get(exercise_id)
    if not exercise:
        return render_template('error.html', message='Exercise not found'), 404
    
    return render_template('exercises/detail.html', exercise=exercise, exercise_id=exercise_id)

@exercises_bp.route('/<exercise_id>/verify', methods=['POST'])
def verify_exercise(exercise_id):
    """Verify if exercise has been completed successfully"""
    
    # This is a simplified verification - in a real scenario, you'd check
    # the actual database state or logs to determine if the exercise was completed
    
    verification_rules = {
        'login_basic': lambda: check_login_bypass(),
        'search_basic': lambda: check_data_extraction(),
        'item_detail': lambda: check_id_injection(),
        'comment_form': lambda: check_comment_injection(),
        'boolean_blind': lambda: check_boolean_injection(),
        'time_blind': lambda: check_time_injection()
    }
    
    if exercise_id in verification_rules:
        success = verification_rules[exercise_id]()
        
        if success:
            # Generate completion token
            import secrets
            token = secrets.token_urlsafe(16)
            session[f'exercise_{exercise_id}_completed'] = True
            session[f'exercise_{exercise_id}_token'] = token
            
            return jsonify({
                'success': True,
                'message': 'Exercise completed successfully!',
                'token': token
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Exercise not yet completed. Keep trying!'
            })
    
    return jsonify({'success': False, 'message': 'Unknown exercise'}), 404

def check_login_bypass():
    """Check if login bypass was successful"""
    # Check recent exercise logs for successful login attempts
    recent_logs = ExerciseLog.query.filter_by(
        exercise_name='login_basic',
        success=True
    ).order_by(ExerciseLog.timestamp.desc()).limit(5).all()
    
    return len(recent_logs) > 0

def check_data_extraction():
    """Check if data extraction was successful"""
    recent_logs = ExerciseLog.query.filter_by(
        exercise_name='search_basic',
        success=True
    ).order_by(ExerciseLog.timestamp.desc()).limit(5).all()
    
    return len(recent_logs) > 0

def check_id_injection():
    """Check if ID injection was successful"""
    recent_logs = ExerciseLog.query.filter_by(
        exercise_name='item_detail',
        success=True
    ).order_by(ExerciseLog.timestamp.desc()).limit(5).all()
    
    return len(recent_logs) > 0

def check_comment_injection():
    """Check if comment injection was successful"""
    recent_logs = ExerciseLog.query.filter_by(
        exercise_name='comment_form',
        success=True
    ).order_by(ExerciseLog.timestamp.desc()).limit(5).all()
    
    return len(recent_logs) > 0

def check_boolean_injection():
    """Check if boolean injection was successful"""
    recent_logs = ExerciseLog.query.filter_by(
        exercise_name='boolean_blind',
        success=True
    ).order_by(ExerciseLog.timestamp.desc()).limit(5).all()
    
    return len(recent_logs) > 0

def check_time_injection():
    """Check if time injection was successful"""
    recent_logs = ExerciseLog.query.filter_by(
        exercise_name='time_blind',
        success=True
    ).order_by(ExerciseLog.timestamp.desc()).limit(5).all()
    
    return len(recent_logs) > 0
