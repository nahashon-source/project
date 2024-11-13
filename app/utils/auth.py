from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User

def admin_required():
    """Decorator to check if current user is an admin"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_admin:
                return jsonify({'error': 'Admin access required'}), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def get_current_user():
    """Helper function to get current authenticated user"""
    current_user_id = get_jwt_identity()
    return User.query.get(current_user_id)