"""
==================================
MANGA GALLERY
AUTH ROUTES
==================================
"""

from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from werkzeug.security import check_password_hash

from database import db
from models.user import User


auth_bp = Blueprint(
    "auth",
    __name__
)


# ==================================
# LOGIN
# ==================================

@auth_bp.post("/login")
def login():

    data = request.get_json(silent=True) or {}

    print("LOGIN DATA:", data)

    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    print("LOGIN USERNAME:", repr(username))
    print("PASSWORD LENGTH:", len(password))

    user = User.query.filter_by(
        username=username
    ).first()

    print("USER FOUND:", user is not None)

    if not user:
        return jsonify({
            "success": False,
            "message": "Identifiants incorrects"
        }), 401

    print("STATUS:", user.status)
    print(
        "PASSWORD CHECK:",
        check_password_hash(
            user.password_hash,
            password
        )
    )

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return jsonify({
            "success": False,
            "message": "Identifiants incorrects"
        }), 401

    if user.status != "active":
        return jsonify({
            "success": False,
            "message": "Compte désactivé"
        }), 403

    from datetime import datetime

    user.last_login = datetime.utcnow()
    db.session.commit()

    access_token = create_access_token(
        identity=str(user.id)
    )

    refresh_token = create_refresh_token(
        identity=str(user.id)
    )

    return jsonify({
        "success": True,
        "message": "Connexion réussie",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200


# ==================================
# CURRENT USER
# ==================================

@auth_bp.get("/me")
@jwt_required()
def me():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (
        TypeError,
        ValueError
    ):
        return jsonify({
            "success": False,
            "message": "Identifiant utilisateur invalide"
        }), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "Utilisateur introuvable"
        }), 404

    return jsonify({
        "success": True,
        "user": user.to_dict()
    }), 200


# ==================================
# LOGOUT
# ==================================

@auth_bp.post("/logout")
@jwt_required()
def logout():

    return jsonify({
        "success": True,
        "message": "Déconnexion réussie"
    }), 200


# ==================================
# REFRESH TOKEN
# ==================================

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    access_token = create_access_token(
        identity=str(user_id)
    )

    return jsonify({
        "success": True,
        "access_token": access_token
    }), 200


# ==================================
# VERIFY SESSION
# ==================================

@auth_bp.get("/verify")
@jwt_required()
def verify():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (
        TypeError,
        ValueError
    ):
        return jsonify({
            "success": False,
            "message": "Identifiant utilisateur invalide"
        }), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "Utilisateur introuvable"
        }), 404

    return jsonify({
        "success": True,
        "user": user.to_dict()
    }), 200


# ==================================
# AUTH STATUS
# ==================================

@auth_bp.get("/status")
def status():

    return jsonify({
        "service": "Authentication",
        "status": "online"
    }), 200