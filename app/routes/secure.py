from flask import Blueprint, render_template, request, jsonify, session, flash
from app import db
from app.models import User, Product, Comment, ExerciseLog
import logging

secure_bp = Blueprint('secure', __name__)

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

@secure_bp.route('/login', methods=['GET', 'POST'])
def login():
    """SECURE: Login form using parameterized queries"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # SECURE CODE: Using parameterized queries (SQLAlchemy ORM)
        # This prevents SQL injection by properly escaping parameters
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            log_exercise_attempt('secure_login', f"username={username}, password={password}", True)
            return render_template('secure/login_success.html', user=user)
        else:
            flash('Invalid credentials', 'error')
            log_exercise_attempt('secure_login', f"username={username}, password={password}", False)
    
    return render_template('secure/login.html')

@secure_bp.route('/search')
def search():
    """SECURE: Product search using parameterized queries"""
    query_param = request.args.get('q', '')
    
    if query_param:
        # SECURE CODE: Using SQLAlchemy ORM with LIKE operator
        # Parameters are properly escaped automatically
        products = Product.query.filter(
            db.or_(
                Product.name.like(f'%{query_param}%'),
                Product.description.like(f'%{query_param}%')
            )
        ).all()
        
        log_exercise_attempt('secure_search', f"query={query_param}", len(products) > 0)
    else:
        products = []
    
    return render_template('secure/search.html', products=products, query=query_param)

@secure_bp.route('/item')
def item_detail():
    """SECURE: Item detail view using ORM"""
    item_id = request.args.get('id', '')
    
    if item_id:
        try:
            # SECURE CODE: Using ORM with proper type conversion
            # SQLAlchemy handles parameter validation and escaping
            product_id = int(item_id)
            product = Product.query.get(product_id)
            
            if product:
                # Get comment count using ORM
                comment_count = Comment.query.filter_by(product_id=product_id).count()
                comments = Comment.query.filter_by(product_id=product_id).all()
                
                log_exercise_attempt('secure_item_detail', f"id={item_id}", True)
                return render_template('secure/item_detail.html', 
                                     product=product, 
                                     comments=comments,
                                     comment_count=comment_count)
            else:
                flash('Product not found', 'error')
                log_exercise_attempt('secure_item_detail', f"id={item_id}", False)
                
        except ValueError:
            flash('Invalid product ID', 'error')
            log_exercise_attempt('secure_item_detail', f"id={item_id}", False)
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
            log_exercise_attempt('secure_item_detail', f"id={item_id}", False)
    
    return render_template('secure/item_detail.html', product=None, comments=[], comment_count=0)

@secure_bp.route('/comment', methods=['GET', 'POST'])
def comment():
    """SECURE: Comment submission using ORM"""
    if request.method == 'POST':
        product_id = request.form.get('product_id', '')
        author = request.form.get('author', '')
        content = request.form.get('content', '')
        
        if product_id and author and content:
            try:
                # SECURE CODE: Using ORM to create new comment
                # All parameters are automatically escaped and validated
                comment = Comment(
                    product_id=int(product_id),
                    author=author.strip(),
                    content=content.strip()
                )
                
                db.session.add(comment)
                db.session.commit()
                
                flash('Comment added successfully!', 'success')
                log_exercise_attempt('secure_comment', f"product_id={product_id}, author={author}, content={content}", True)
                
            except ValueError:
                flash('Invalid product ID', 'error')
                log_exercise_attempt('secure_comment', f"product_id={product_id}, author={author}, content={content}", False)
            except Exception as e:
                flash(f'Error adding comment: {str(e)}', 'error')
                log_exercise_attempt('secure_comment', f"product_id={product_id}, author={author}, content={content}", False)
    
    # Get all products using ORM
    products = Product.query.all()
    
    return render_template('secure/comment.html', products=products)

@secure_bp.route('/boolean')
def boolean_blind():
    """SECURE: Boolean-based query using ORM"""
    user_id = request.args.get('user_id', '')
    
    if user_id:
        try:
            # SECURE CODE: Using ORM with proper validation
            user_id_int = int(user_id)
            user = User.query.get(user_id_int)
            
            # Check if admin exists using ORM
            admin_exists = User.query.filter_by(role='admin').count() > 0
            
            if user:
                response = "User found and admin exists" if admin_exists else "User found but no admin exists"
                log_exercise_attempt('secure_boolean', f"user_id={user_id}", True)
            else:
                response = "User not found"
                log_exercise_attempt('secure_boolean', f"user_id={user_id}", False)
                
            return jsonify({'result': response, 'user_id': user_id})
            
        except ValueError:
            log_exercise_attempt('secure_boolean', f"user_id={user_id}", False)
            return jsonify({'error': 'Invalid user ID'}), 400
        except Exception as e:
            log_exercise_attempt('secure_boolean', f"user_id={user_id}", False)
            return jsonify({'error': str(e)}), 500
    
    return render_template('secure/boolean_blind.html')

@secure_bp.route('/time')
def time_blind():
    """SECURE: Time-based query using ORM"""
    user_id = request.args.get('user_id', '')
    
    if user_id:
        import time
        start_time = time.time()
        
        try:
            # SECURE CODE: Using ORM with proper validation
            user_id_int = int(user_id)
            user = User.query.get(user_id_int)
            
            # Check admin existence using ORM
            admin_exists = User.query.filter_by(role='admin').count() > 0
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if user:
                response = f"User found (response time: {response_time:.3f}s)"
                log_exercise_attempt('secure_time', f"user_id={user_id}", True)
            else:
                response = f"User not found (response time: {response_time:.3f}s)"
                log_exercise_attempt('secure_time', f"user_id={user_id}", False)
                
            return jsonify({'result': response, 'response_time': response_time})
            
        except ValueError:
            log_exercise_attempt('secure_time', f"user_id={user_id}", False)
            return jsonify({'error': 'Invalid user ID'}), 400
        except Exception as e:
            log_exercise_attempt('secure_time', f"user_id={user_id}", False)
            return jsonify({'error': str(e)}), 500
    
    return render_template('secure/time_blind.html')
