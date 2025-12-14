from flask import Blueprint, render_template, request, jsonify, session, flash
from app import db
from app.models import User, Product, Comment, ExerciseLog
import sqlite3
import time
import logging

vulnerable_bp = Blueprint('vulnerable', __name__)

def log_exercise_attempt(exercise_name, user_input, success=False):
    """Log exercise attempts for tracking"""
    log = ExerciseLog(
        exercise_name=exercise_name,
        user_input=user_input,
        success=success,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

@vulnerable_bp.route('/login', methods=['GET', 'POST'])
def login():
    """VULNERABLE: Login form with SQL injection vulnerability"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABLE CODE: String concatenation in SQL query
        # This is intentionally vulnerable for educational purposes
        # DO NOT use this pattern in production code!
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            # Execute the vulnerable query
            conn = sqlite3.connect('data/lab.db')
            cursor = conn.cursor()
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()
            
            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['role'] = user[3]
                flash('Login successful!', 'success')
                log_exercise_attempt('login_basic', f"username={username}, password={password}", True)
                return render_template('vulnerable/login_success.html', user=user)
            else:
                flash('Invalid credentials', 'error')
                log_exercise_attempt('login_basic', f"username={username}, password={password}", False)
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
            log_exercise_attempt('login_basic', f"username={username}, password={password}", False)
    
    return render_template('vulnerable/login.html')

@vulnerable_bp.route('/search')
def search():
    """VULNERABLE: Product search with SQL injection"""
    query_param = request.args.get('q', '')
    
    if query_param:
        # VULNERABLE CODE: Direct string interpolation in SQL
        # This allows SQL injection through the search parameter
        sql_query = f"SELECT * FROM products WHERE name LIKE '%{query_param}%' OR description LIKE '%{query_param}%'"
        
        try:
            conn = sqlite3.connect('data/lab.db')
            cursor = conn.cursor()
            cursor.execute(sql_query)
            products = cursor.fetchall()
            conn.close()
            
            log_exercise_attempt('search_basic', f"query={query_param}", len(products) > 0)
            
        except Exception as e:
            products = []
            flash(f'Search error: {str(e)}', 'error')
            log_exercise_attempt('search_basic', f"query={query_param}", False)
    else:
        products = []
    
    return render_template('vulnerable/search.html', products=products, query=query_param)

@vulnerable_bp.route('/item')
def item_detail():
    """VULNERABLE: Item detail view with numeric SQL injection"""
    item_id = request.args.get('id', '')
    
    if item_id:
        # VULNERABLE CODE: Numeric parameter without proper validation
        # This can be exploited with stacked queries or other techniques
        sql_query = f"SELECT p.*, COUNT(c.id) as comment_count FROM products p LEFT JOIN comments c ON p.id = c.product_id WHERE p.id = {item_id} GROUP BY p.id"
        
        try:
            conn = sqlite3.connect('data/lab.db')
            cursor = conn.cursor()
            cursor.execute(sql_query)
            product = cursor.fetchone()
            
            # Get comments for this product
            comment_query = f"SELECT * FROM comments WHERE product_id = {item_id}"
            cursor.execute(comment_query)
            comments = cursor.fetchall()
            conn.close()
            
            if product:
                log_exercise_attempt('item_detail', f"id={item_id}", True)
                return render_template('vulnerable/item_detail.html', product=product, comments=comments)
            else:
                flash('Product not found', 'error')
                log_exercise_attempt('item_detail', f"id={item_id}", False)
                
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
            log_exercise_attempt('item_detail', f"id={item_id}", False)
    
    return render_template('vulnerable/item_detail.html', product=None, comments=[])

@vulnerable_bp.route('/comment', methods=['GET', 'POST'])
def comment():
    """VULNERABLE: Comment submission with SQL injection"""
    if request.method == 'POST':
        product_id = request.form.get('product_id', '')
        author = request.form.get('author', '')
        content = request.form.get('content', '')
        
        if product_id and author and content:
            # VULNERABLE CODE: Multiple parameters without proper sanitization
            # This allows injection through any of the form fields
            sql_query = f"INSERT INTO comments (product_id, author, content) VALUES ({product_id}, '{author}', '{content}')"
            
            try:
                conn = sqlite3.connect('data/lab.db')
                cursor = conn.cursor()
                cursor.execute(sql_query)
                conn.commit()
                conn.close()
                
                flash('Comment added successfully!', 'success')
                log_exercise_attempt('comment_form', f"product_id={product_id}, author={author}, content={content}", True)
                
            except Exception as e:
                flash(f'Error adding comment: {str(e)}', 'error')
                log_exercise_attempt('comment_form', f"product_id={product_id}, author={author}, content={content}", False)
    
    # Get all products for the form
    conn = sqlite3.connect('data/lab.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    
    return render_template('vulnerable/comment.html', products=products)

@vulnerable_bp.route('/boolean')
def boolean_blind():
    """VULNERABLE: Boolean-based blind SQL injection"""
    user_id = request.args.get('user_id', '')
    
    if user_id:
        # VULNERABLE CODE: Boolean-based blind injection
        # This returns different results based on boolean conditions
        sql_query = f"SELECT * FROM users WHERE id = {user_id} AND (SELECT COUNT(*) FROM users WHERE role = 'admin') > 0"
        
        try:
            conn = sqlite3.connect('data/lab.db')
            cursor = conn.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchone()
            conn.close()
            
            # Return different responses based on the boolean condition
            if result:
                response = "User found and admin exists"
                log_exercise_attempt('boolean_blind', f"user_id={user_id}", True)
            else:
                response = "User not found or no admin exists"
                log_exercise_attempt('boolean_blind', f"user_id={user_id}", False)
                
            return jsonify({'result': response, 'user_id': user_id})
            
        except Exception as e:
            log_exercise_attempt('boolean_blind', f"user_id={user_id}", False)
            return jsonify({'error': str(e)}), 500
    
    return render_template('vulnerable/boolean_blind.html')

@vulnerable_bp.route('/time')
def time_blind():
    """VULNERABLE: Time-based blind SQL injection"""
    user_id = request.args.get('user_id', '')
    
    if user_id:
        # VULNERABLE CODE: Time-based blind injection
        # This uses timing to extract information
        sql_query = f"SELECT * FROM users WHERE id = {user_id} AND (SELECT CASE WHEN (SELECT COUNT(*) FROM users WHERE role = 'admin') > 0 THEN 1 ELSE 0 END) = 1"
        
        start_time = time.time()
        
        try:
            conn = sqlite3.connect('data/lab.db')
            cursor = conn.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchone()
            conn.close()
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Simulate different response times based on conditions
            if result:
                response = f"User found (response time: {response_time:.3f}s)"
                log_exercise_attempt('time_blind', f"user_id={user_id}", True)
            else:
                response = f"User not found (response time: {response_time:.3f}s)"
                log_exercise_attempt('time_blind', f"user_id={user_id}", False)
                
            return jsonify({'result': response, 'response_time': response_time})
            
        except Exception as e:
            log_exercise_attempt('time_blind', f"user_id={user_id}", False)
            return jsonify({'error': str(e)}), 500
    
    return render_template('vulnerable/time_blind.html')
