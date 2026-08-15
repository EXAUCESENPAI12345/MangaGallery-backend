from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def jwt_required_middleware():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request(); return function(*args, **kwargs)
        return wrapper
    return decorator

def current_user():
    try: user_id=int(get_jwt_identity())
    except (TypeError,ValueError): return None
    return User.query.get(user_id)

def authenticated_user():
    user=current_user()
    return user if user else (jsonify(success=False,message="Utilisateur introuvable"),404)

def active_user():
    user=authenticated_user()
    if isinstance(user,tuple): return user
    return user if user.status=="active" else (jsonify(success=False,message="Compte suspendu"),403)

def verified_user():
    user=active_user()
    if isinstance(user,tuple): return user
    return user if user.is_verified else (jsonify(success=False,message="Compte non vérifié"),403)

def validate_token():
    try: verify_jwt_in_request(); return True
    except Exception: return False
