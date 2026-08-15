from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User


def current_user():
    try:
        user_id = int(get_jwt_identity())
    except (TypeError, ValueError):
        return None
    return User.query.get(user_id)


def require_admin(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user or user.status != "active":
            return jsonify(success=False, message="Authentification requise"), 401
        if user.id != 1 and user.role != "admin":
            return jsonify(success=False, message="Accès réservé à l'administrateur"), 403
        return fn(*args, **kwargs)
    return wrapper
