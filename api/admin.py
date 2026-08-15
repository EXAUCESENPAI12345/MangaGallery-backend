from datetime import datetime

from flask import Blueprint, request

from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required
)

from database import db
from models.user import User
from models.admin import Admin
from models.manga import Manga
from models.chapter import Chapter
from models.comment import Comment
from models.notification import Notification


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
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
# ADMIN ACCESS
# ==================================

def admin_required():

    claims = get_jwt()

    role = claims.get(
        "role"
    )

    return role in {
        "admin",
        "super_admin"
    }


def require_admin():

    if not admin_required():

        return error_response(
            "Accès réservé aux administrateurs.",
            "ADMIN_ACCESS_REQUIRED",
            403
        )

    return None


# ==================================
# ADMIN PROFILE
# ==================================

@admin_bp.get("/me")
@jwt_required()
def admin_profile():

    access_error = require_admin()

    if access_error:

        return access_error


    user_id = get_jwt_identity()

    user = User.query.get(
        int(user_id)
    )


    if not user:

        return error_response(
            "Administrateur introuvable.",
            "ADMIN_NOT_FOUND",
            404
        )


    return success_response(

        "Profil administrateur récupéré.",

        {

            "admin":
                user.to_dict()

        }

    )


# ==================================
# DASHBOARD STATISTICS
# ==================================

@admin_bp.get("/stats")
@jwt_required()
def dashboard_stats():

    access_error = require_admin()

    if access_error:

        return access_error


    total_users = User.query.count()

    active_users = User.query.filter_by(
        status="active"
    ).count()

    blocked_users = User.query.filter_by(
        status="blocked"
    ).count()

    total_mangas = Manga.query.count()

    total_chapters = Chapter.query.count()

    total_comments = Comment.query.count()

    total_notifications = Notification.query.count()


    return success_response(

        "Statistiques récupérées.",

        {

            "users": {

                "total":
                    total_users,

                "active":
                    active_users,

                "blocked":
                    blocked_users

            },

            "content": {

                "mangas":
                    total_mangas,

                "chapters":
                    total_chapters,

                "comments":
                    total_comments

            },

            "notifications":
                total_notifications

        }

    )


# ==================================
# LIST USERS
# ==================================

@admin_bp.get("/users")
@jwt_required()
def list_users():

    access_error = require_admin()

    if access_error:

        return access_error


    page = request.args.get(
        "page",
        1,
        type=int
    )

    per_page = request.args.get(
        "per_page",
        20,
        type=int
    )


    page = max(
        page,
        1
    )

    per_page = min(
        max(
            per_page,
            1
        ),
        100
    )


    pagination = User.query.order_by(
        User.created_at.desc()
    ).paginate(

        page=page,

        per_page=per_page,

        error_out=False

    )


    return success_response(

        "Utilisateurs récupérés.",

        {

            "items": [

                user.to_dict()

                for user
                in pagination.items

            ],

            "pagination": {

                "page":
                    pagination.page,

                "per_page":
                    pagination.per_page,

                "total":
                    pagination.total,

                "pages":
                    pagination.pages,

                "has_next":
                    pagination.has_next,

                "has_previous":
                    pagination.has_prev

            }

        }

    )
    
    # ==================================
# UPDATE USER STATUS
# ==================================

@admin_bp.patch(
    "/users/<int:user_id>/status"
)
@jwt_required()
def update_user_status(user_id):

    access_error = require_admin()

    if access_error:
        return access_error

    user = User.query.get(user_id)

    if not user:
        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404
        )

    data = request.get_json(
        silent=True
    ) or {}

    status = str(
        data.get(
            "status",
            ""
        )
    ).strip().lower()

    allowed_statuses = {
        "active",
        "blocked",
        "suspended"
    }

    if status not in allowed_statuses:
        return error_response(
            "Statut utilisateur invalide.",
            "INVALID_STATUS",
            400
        )

    user.status = status

    user.updated_at = datetime.utcnow()

    db.session.commit()

    return success_response(
        "Statut utilisateur mis à jour.",
        {
            "user":
                user.to_dict()
        }
    )


# ==================================
# UPDATE USER ROLE
# ==================================

@admin_bp.patch(
    "/users/<int:user_id>/role"
)
@jwt_required()
def update_user_role(user_id):

    access_error = require_admin()

    if access_error:
        return access_error

    user = User.query.get(user_id)

    if not user:
        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404
        )

    data = request.get_json(
        silent=True
    ) or {}

    role = str(
        data.get(
            "role",
            ""
        )
    ).strip().lower()

    allowed_roles = {
        "user",
        "moderator",
        "admin"
    }

    if role not in allowed_roles:
        return error_response(
            "Rôle utilisateur invalide.",
            "INVALID_ROLE",
            400
        )

    user.role = role

    user.updated_at = datetime.utcnow()

    db.session.commit()

    return success_response(
        "Rôle utilisateur mis à jour.",
        {
            "user":
                user.to_dict()
        }
    )


# ==================================
# DELETE USER
# ==================================

@admin_bp.delete(
    "/users/<int:user_id>"
)
@jwt_required()
def delete_user(user_id):

    access_error = require_admin()

    if access_error:
        return access_error

    current_user_id = int(
        get_jwt_identity()
    )

    if current_user_id == user_id:
        return error_response(
            "Vous ne pouvez pas supprimer votre propre compte administrateur.",
            "SELF_DELETE_FORBIDDEN",
            403
        )

    user = User.query.get(user_id)

    if not user:
        return error_response(
            "Utilisateur introuvable.",
            "USER_NOT_FOUND",
            404
        )

    user.status = "deleted"

    user.email = None

    user.password_hash = None

    user.updated_at = datetime.utcnow()

    db.session.commit()

    return success_response(
        "Utilisateur supprimé.",
        None
    )


# ==================================
# LIST ADMINS
# ==================================

@admin_bp.get("/admins")
@jwt_required()
def list_admins():

    access_error = require_admin()

    if access_error:
        return access_error

    admins = Admin.query.order_by(
        Admin.created_at.desc()
    ).all()

    return success_response(
        "Administrateurs récupérés.",
        {
            "items": [
                admin.to_dict()
                for admin in admins
            ],
            "total":
                len(admins)
        }
    )


# ==================================
# LIST MANGAS
# ==================================

@admin_bp.get("/mangas")
@jwt_required()
def admin_mangas():

    access_error = require_admin()

    if access_error:
        return access_error

    mangas = Manga.query.order_by(
        Manga.updated_at.desc()
    ).all()

    return success_response(
        "Mangas récupérés.",
        {
            "items": [
                manga.to_dict()
                for manga in mangas
            ],
            "total":
                len(mangas)
        }
    )


# ==================================
# LIST COMMENTS
# ==================================

@admin_bp.get("/comments")
@jwt_required()
def admin_comments():

    access_error = require_admin()

    if access_error:
        return access_error

    comments = Comment.query.order_by(
        Comment.created_at.desc()
    ).limit(100).all()

    return success_response(
        "Commentaires récupérés.",
        {
            "items": [
                comment.to_dict()
                for comment in comments
            ],
            "total":
                len(comments)
        }
    )
    
    # ==================================
# DELETE COMMENT
# ==================================

@admin_bp.delete(
    "/comments/<int:comment_id>"
)
@jwt_required()
def admin_delete_comment(comment_id):

    access_error = require_admin()

    if access_error:
        return access_error

    comment = Comment.query.get(
        comment_id
    )

    if not comment:
        return error_response(
            "Commentaire introuvable.",
            "COMMENT_NOT_FOUND",
            404
        )

    db.session.delete(
        comment
    )

    db.session.commit()

    return success_response(
        "Commentaire supprimé.",
        None
    )


# ==================================
# CREATE NOTIFICATION FOR USER
# ==================================

@admin_bp.post(
    "/users/<int:user_id>/notifications"
)
@jwt_required()
def admin_create_notification(user_id):

    access_error = require_admin()

    if access_error:
        return access_error

    user = User.query.get(
        user_id
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

    title = str(
        data.get(
            "title",
            ""
        )
    ).strip()

    message = str(
        data.get(
            "message",
            ""
        )
    ).strip()

    notification_type = str(
        data.get(
            "type",
            "system"
        )
    ).strip().lower()

    if not title:
        return error_response(
            "Le titre est obligatoire.",
            "TITLE_REQUIRED",
            400
        )

    if not message:
        return error_response(
            "Le message est obligatoire.",
            "MESSAGE_REQUIRED",
            400
        )

    notification = Notification(

        user_id=user.id,

        title=title,

        message=message,

        type=notification_type,

        is_read=False,

        data=data.get(
            "data"
        )

    )

    db.session.add(
        notification
    )

    db.session.commit()

    return success_response(

        "Notification envoyée à l'utilisateur.",

        {
            "notification":
                notification.to_dict()
        },

        201

    )


# ==================================
# SYSTEM INFORMATION
# ==================================

@admin_bp.get(
    "/system"
)
@jwt_required()
def system_information():

    access_error = require_admin()

    if access_error:
        return access_error

    return success_response(

        "Informations système récupérées.",

        {

            "application": {

                "name":
                    "Manga Gallery",

                "environment":
                    "production"

            },

            "database": {

                "status":
                    "online"

            },

            "api": {

                "status":
                    "online"

            },

            "services": [

                {
                    "name":
                        "API",

                    "description":
                        "Service API principal",

                    "status":
                        "online",

                    "icon":
                        "server"
                },

                {
                    "name":
                        "Base de données",

                    "description":
                        "PostgreSQL",

                    "status":
                        "online",

                    "icon":
                        "database"
                }

            ]

        }

    )


# ==================================
# REGISTER BLUEPRINT
# ==================================

def register_admin_routes(app):

    app.register_blueprint(
        admin_bp
    )

    return app