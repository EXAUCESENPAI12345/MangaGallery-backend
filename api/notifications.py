from flask import Blueprint, request

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from database import db
from models.notification import Notification


notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/api/notifications"
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
# LIST NOTIFICATIONS
# ==================================

@notifications_bp.get("")
@jwt_required()
def list_notifications():

    user_id = get_jwt_identity()

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


    pagination = Notification.query.filter(

        Notification.user_id ==
        int(user_id)

    ).order_by(

        Notification.created_at.desc()

    ).paginate(

        page=page,

        per_page=per_page,

        error_out=False

    )


    return success_response(

        "Notifications récupérées.",

        {

            "items": [

                notification.to_dict()

                for notification
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
# UNREAD COUNT
# ==================================

@notifications_bp.get(
    "/unread-count"
)
@jwt_required()
def unread_count():

    user_id = get_jwt_identity()

    count = Notification.query.filter(

        Notification.user_id ==
        int(user_id),

        Notification.is_read ==
        False

    ).count()


    return success_response(

        "Nombre de notifications non lues récupéré.",

        {

            "unread":
                count

        }

    )


# ==================================
# GET NOTIFICATION
# ==================================

@notifications_bp.get(
    "/<int:notification_id>"
)
@jwt_required()
def get_notification(
    notification_id
):

    user_id = get_jwt_identity()

    notification = Notification.query.filter(

        Notification.id ==
        notification_id,

        Notification.user_id ==
        int(user_id)

    ).first()


    if not notification:

        return error_response(
            "Notification introuvable.",
            "NOTIFICATION_NOT_FOUND",
            404
        )


    return success_response(

        "Notification récupérée.",

        {

            "notification":
                notification.to_dict()

        }

    )
    
    # ==================================
# MARK AS READ
# ==================================

@notifications_bp.patch(
    "/<int:notification_id>/read"
)
@jwt_required()
def mark_as_read(
    notification_id
):

    user_id = get_jwt_identity()

    notification = Notification.query.filter(

        Notification.id ==
        notification_id,

        Notification.user_id ==
        int(user_id)

    ).first()


    if not notification:

        return error_response(
            "Notification introuvable.",
            "NOTIFICATION_NOT_FOUND",
            404
        )


    notification.mark_as_read()

    db.session.commit()


    return success_response(

        "Notification marquée comme lue.",

        {

            "notification":
                notification.to_dict()

        }

    )


# ==================================
# MARK ALL AS READ
# ==================================

@notifications_bp.patch(
    "/read-all"
)
@jwt_required()
def mark_all_as_read():

    user_id = get_jwt_identity()

    notifications = Notification.query.filter(

        Notification.user_id ==
        int(user_id),

        Notification.is_read ==
        False

    ).all()


    for notification in notifications:

        notification.mark_as_read()


    db.session.commit()


    return success_response(

        "Toutes les notifications ont été marquées comme lues.",

        {

            "updated":
                len(notifications)

        }

    )


# ==================================
# DELETE NOTIFICATION
# ==================================

@notifications_bp.delete(
    "/<int:notification_id>"
)
@jwt_required()
def delete_notification(
    notification_id
):

    user_id = get_jwt_identity()

    notification = Notification.query.filter(

        Notification.id ==
        notification_id,

        Notification.user_id ==
        int(user_id)

    ).first()


    if not notification:

        return error_response(
            "Notification introuvable.",
            "NOTIFICATION_NOT_FOUND",
            404
        )


    db.session.delete(
        notification
    )

    db.session.commit()


    return success_response(

        "Notification supprimée.",

        None

    )
    
    # ==================================
# CREATE NOTIFICATION
# ==================================

@notifications_bp.post("")
@jwt_required()
def create_notification():

    user_id = get_jwt_identity()

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
            "Le titre de la notification est obligatoire.",
            "TITLE_REQUIRED",
            400
        )


    if not message:

        return error_response(
            "Le message de la notification est obligatoire.",
            "MESSAGE_REQUIRED",
            400
        )


    notification = Notification(

        user_id=int(
            user_id
        ),

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

        "Notification créée avec succès.",

        {

            "notification":
                notification.to_dict()

        },

        201

    )


# ==================================
# REGISTER BLUEPRINT
# ==================================

def register_notification_routes(app):

    app.register_blueprint(
        notifications_bp
    )

    return app