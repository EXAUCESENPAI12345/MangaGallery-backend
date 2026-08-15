from flask import Blueprint, request

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from database import db
from models.user import User


users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/api/users"
)


# ==================================
# RESPONSE HELPERS
# ==================================

def success_response(
    message,
    data=None,
    status=200
):

    return {

        "success": True,

        "message": message,

        "data": data

    }, status


def error_response(
    message,
    code,
    status=400
):

    return {

        "success": False,

        "error": {

            "code": code,

            "message": message

        }

    }, status


# ==================================
# CURRENT USER PROFILE
# ==================================

@users_bp.get("/me")
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()

    user = User.query.get(
        int(user_id)
    )

    if not user:

        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404
        )

    return success_response(

        "Profil récupéré.",

        {
            "user":
                user.to_dict()
        }

    )


# ==================================
# UPDATE CURRENT USER
# ==================================

@users_bp.put("/me")
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    user = User.query.get(
        int(user_id)
    )

    if not user:

        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404
        )


    data = request.get_json(
        silent=True
    ) or {}


    allowed_fields = {

        "username",
        "first_name",
        "last_name",
        "photo_url"

    }


    for field in allowed_fields:

        if field not in data:

            continue

        value = data.get(
            field
        )

        if value is None:

            setattr(
                user,
                field,
                None
            )

            continue

        value = str(
            value
        ).strip()

        setattr(
            user,
            field,
            value or None
        )


    db.session.commit()


    return success_response(

        "Profil mis à jour.",

        {
            "user":
                user.to_dict()
        }

    )


# ==================================
# USER BY ID
# ==================================

@users_bp.get("/<int:user_id>")
@jwt_required()
def get_user(
    user_id
):

    user = User.query.get(
        user_id
    )

    if not user:

        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404
        )


    return success_response(

        "Utilisateur récupéré.",

        {
            "user":
                user.to_dict()
        }

    )
    
    # ==================================
# DELETE CURRENT USER
# ==================================

@users_bp.delete("/me")
@jwt_required()
def delete_account():

    user_id = get_jwt_identity()

    user = User.query.get(
        int(user_id)
    )

    if not user:

        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404
        )


    user.status = "deleted"

    user.email = None

    user.password_hash = None

    user.updated_at = (
        __import__(
            "datetime"
        ).datetime.utcnow()
    )


    db.session.commit()


    return success_response(

        "Compte supprimé avec succès.",

        None

    )


# ==================================
# USER NOTIFICATIONS COUNT
# ==================================

@users_bp.get(
    "/me/notifications/count"
)
@jwt_required()
def notification_count():

    from models.notification import Notification

    user_id = get_jwt_identity()

    count = Notification.query.filter_by(
        user_id=int(user_id),
        is_read=False
    ).count()


    return success_response(

        "Nombre de notifications récupéré.",

        {
            "unread":
                count
        }

    )


# ==================================
# REGISTER BLUEPRINT
# ==================================

def register_users_routes(app):

    app.register_blueprint(
        users_bp
    )

    return app
    
    # ==================================
# UPDATE USER PHOTO
# ==================================

@users_bp.patch("/me/photo")
@jwt_required()
def update_photo():

    user_id = get_jwt_identity()

    user = User.query.get(
        int(user_id)
    )

    if not user:

        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404
        )


    data = request.get_json(
        silent=True
    ) or {}


    photo_url = data.get(
        "photo_url"
    )


    if photo_url is None:

        return error_response(
            "L'URL de la photo est obligatoire.",
            "PHOTO_URL_REQUIRED",
            400
        )


    photo_url = str(
        photo_url
    ).strip()


    if not photo_url:

        return error_response(
            "L'URL de la photo est invalide.",
            "INVALID_PHOTO_URL",
            400
        )


    user.photo_url = photo_url

    db.session.commit()


    return success_response(

        "Photo mise à jour.",

        {
            "user":
                user.to_dict()
        }

    )


# ==================================
# REGISTER BLUEPRINT
# ==================================

def register_users_routes(app):

    app.register_blueprint(
        users_bp
    )

    return app