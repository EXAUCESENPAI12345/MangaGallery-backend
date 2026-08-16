from datetime import datetime, timedelta

from flask import Blueprint, request

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from database import db
from models.user import User


# ==================================
# BLUEPRINT
# ==================================

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth",
)


# ==================================
# RESPONSE HELPERS
# ==================================

def success_response(message, data=None, status=200):
    return {
        "success": True,
        "message": message,
        "data": data,
    }, status


def error_response(message, code, status=400):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }, status


# ==================================
# REGISTER
# ==================================

@auth_bp.post("/register")
def register():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    email = str(
        data.get("email", "")
    ).strip().lower()

    password = str(
        data.get("password", "")
    )

    if not username:
        return error_response(
            "Le nom d'utilisateur est obligatoire.",
            "USERNAME_REQUIRED",
            400,
        )

    if not email:
        return error_response(
            "L'adresse e-mail est obligatoire.",
            "EMAIL_REQUIRED",
            400,
        )

    if len(password) < 8:
        return error_response(
            "Le mot de passe doit contenir au moins 8 caractères.",
            "WEAK_PASSWORD",
            400,
        )

    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return error_response(
            "Cette adresse e-mail est déjà utilisée.",
            "EMAIL_EXISTS",
            409,
        )

    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        return error_response(
            "Ce nom d'utilisateur est déjà utilisé.",
            "USERNAME_EXISTS",
            409,
        )

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role="user",
        role_id=None,
        status="active",
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.session.add(user)
    db.session.commit()

    return success_response(
        "Compte créé avec succès.",
        {
            "user": user.to_dict(),
        },
        201,
    )


# ==================================
# LOGIN
# ==================================

@auth_bp.post("/login")
def login():

    data = request.get_json(silent=True) or {}

    email = str(
        data.get("email", "")
    ).strip().lower()

    password = str(
        data.get("password", "")
    )

    if not email or not password:
        return error_response(
            "E-mail et mot de passe obligatoires.",
            "CREDENTIALS_REQUIRED",
            400,
        )

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return error_response(
            "Identifiants incorrects.",
            "INVALID_CREDENTIALS",
            401,
        )

    if not user.password_hash:
        return error_response(
            "Identifiants incorrects.",
            "INVALID_CREDENTIALS",
            401,
        )

    if not check_password_hash(
        user.password_hash,
        password,
    ):
        return error_response(
            "Identifiants incorrects.",
            "INVALID_CREDENTIALS",
            401,
        )

    if user.status != "active":
        return error_response(
            "Ce compte n'est pas actif.",
            "ACCOUNT_INACTIVE",
            403,
        )

    user.last_login = datetime.utcnow()
    db.session.commit()

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role,
        },
        expires_delta=timedelta(hours=1),
    )

    refresh_token = create_refresh_token(
        identity=str(user.id),
    )

    return success_response(
        "Connexion réussie.",
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "user": user.to_dict(),
        },
    )


# ==================================
# CURRENT USER
# ==================================

@auth_bp.get("/me")
@jwt_required()
def me():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return error_response(
            "Identifiant utilisateur invalide.",
            "INVALID_USER_ID",
            401,
        )

    user = User.query.get(user_id)

    if not user:
        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404,
        )

    return success_response(
        "Utilisateur récupéré.",
        {
            "user": user.to_dict(),
        },
    )


# ==================================
# REFRESH TOKEN
# ==================================

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    access_token = create_access_token(
        identity=str(user_id),
        expires_delta=timedelta(hours=1),
    )

    return success_response(
        "Token renouvelé.",
        {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        },
    )


# ==================================
# VERIFY SESSION
# ==================================

@auth_bp.get("/verify")
@jwt_required()
def verify():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return error_response(
            "Identifiant utilisateur invalide.",
            "INVALID_USER_ID",
            401,
        )

    user = User.query.get(user_id)

    if not user:
        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404,
        )

    if user.status != "active":
        return error_response(
            "Ce compte n'est pas actif.",
            "ACCOUNT_INACTIVE",
            403,
        )

    return success_response(
        "Session valide.",
        {
            "user": user.to_dict(),
        },
    )


# ==================================
# LOGOUT
# ==================================

@auth_bp.post("/logout")
@jwt_required()
def logout():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return error_response(
            "Identifiant utilisateur invalide.",
            "INVALID_USER_ID",
            401,
        )

    user = User.query.get(user_id)

    if not user:
        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404,
        )

    return success_response(
        "Déconnexion effectuée.",
        None,
    )


# ==================================
# CHANGE PASSWORD
# ==================================

@auth_bp.post("/change-password")
@jwt_required()
def change_password():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return error_response(
            "Identifiant utilisateur invalide.",
            "INVALID_USER_ID",
            401,
        )

    data = request.get_json(silent=True) or {}

    current_password = str(
        data.get("current_password", "")
    )

    new_password = str(
        data.get("new_password", "")
    )

    if not current_password or not new_password:
        return error_response(
            "Les deux mots de passe sont obligatoires.",
            "PASSWORD_REQUIRED",
            400,
        )

    if len(new_password) < 8:
        return error_response(
            "Le nouveau mot de passe doit contenir au moins 8 caractères.",
            "WEAK_PASSWORD",
            400,
        )

    user = User.query.get(user_id)

    if not user:
        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404,
        )

    if not user.password_hash:
        return error_response(
            "Aucun mot de passe n'est configuré pour ce compte.",
            "PASSWORD_NOT_CONFIGURED",
            400,
        )

    if not check_password_hash(
        user.password_hash,
        current_password,
    ):
        return error_response(
            "Le mot de passe actuel est incorrect.",
            "INVALID_PASSWORD",
            401,
        )

    user.password_hash = generate_password_hash(
        new_password
    )

    user.updated_at = datetime.utcnow()

    db.session.commit()

    return success_response(
        "Mot de passe modifié avec succès.",
        None,
    )


# ==================================
# AUTH STATUS
# ==================================

@auth_bp.get("/status")
def status():

    return success_response(
        "Service d'authentification opérationnel.",
        {
            "service": "Authentication",
            "status": "online",
        },
    )


# ==================================
# REGISTER BLUEPRINT
# ==================================

def register_auth_routes(app):

    app.register_blueprint(
        auth_bp
    )

    return app
