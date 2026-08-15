from flask import Blueprint, request

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from database import db
from models.comment import Comment


comments_bp = Blueprint(
    "comments",
    __name__,
    url_prefix="/api/comments"
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
# LIST COMMENTS
# ==================================

@comments_bp.get("")
def list_comments():

    manga_id = request.args.get(
        "manga_id",
        type=int
    )

    chapter_id = request.args.get(
        "chapter_id",
        type=int
    )

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


    query = Comment.query.filter(
        Comment.status == "visible"
    )


    if manga_id is not None:

        query = query.filter(
            Comment.manga_id ==
            manga_id
        )


    if chapter_id is not None:

        query = query.filter(
            Comment.chapter_id ==
            chapter_id
        )


    pagination = query.order_by(
        Comment.created_at.desc()
    ).paginate(

        page=page,

        per_page=per_page,

        error_out=False

    )


    items = []


    for comment in pagination.items:

        item = comment.to_dict()

        if comment.user:

            item["user"] = {

                "id":
                    comment.user.id,

                "username":
                    comment.user.username,

                "first_name":
                    comment.user.first_name,

                "last_name":
                    comment.user.last_name,

                "photo_url":
                    comment.user.photo_url

            }

        else:

            item["user"] = None


        items.append(
            item
        )


    return success_response(

        "Commentaires récupérés.",

        {

            "items":
                items,

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
# CREATE COMMENT
# ==================================

@comments_bp.post("")
@jwt_required()
def create_comment():

    user_id = get_jwt_identity()

    data = request.get_json(
        silent=True
    ) or {}


    content = str(
        data.get(
            "content",
            ""
        )
    ).strip()


    if not content:

        return error_response(
            "Le commentaire ne peut pas être vide.",
            "CONTENT_REQUIRED",
            400
        )


    if len(content) > 2000:

        return error_response(
            "Le commentaire est trop long.",
            "CONTENT_TOO_LONG",
            400
        )


    manga_id = data.get(
        "manga_id"
    )

    chapter_id = data.get(
        "chapter_id"
    )


    if manga_id is None and chapter_id is None:

        return error_response(
            "Un manga ou un chapitre est obligatoire.",
            "TARGET_REQUIRED",
            400
        )


    comment = Comment(

        user_id=int(
            user_id
        ),

        manga_id=int(
            manga_id
        ) if manga_id is not None
        else None,

        chapter_id=int(
            chapter_id
        ) if chapter_id is not None
        else None,

        content=content,

        status="visible"

    )


    db.session.add(
        comment
    )

    db.session.commit()


    return success_response(

        "Commentaire publié avec succès.",

        {
            "comment":
                comment.to_dict()
        },

        201

    )
    
    # ==================================
# UPDATE COMMENT
# ==================================

@comments_bp.put(
    "/<int:comment_id>"
)
@jwt_required()
def update_comment(
    comment_id
):

    user_id = get_jwt_identity()

    comment = Comment.query.get(
        comment_id
    )

    if not comment:

        return error_response(
            "Commentaire introuvable.",
            "COMMENT_NOT_FOUND",
            404
        )


    if comment.user_id != int(
        user_id
    ):

        return error_response(
            "Vous ne pouvez modifier que votre propre commentaire.",
            "FORBIDDEN",
            403
        )


    data = request.get_json(
        silent=True
    ) or {}


    content = str(
        data.get(
            "content",
            ""
        )
    ).strip()


    if not content:

        return error_response(
            "Le commentaire ne peut pas être vide.",
            "CONTENT_REQUIRED",
            400
        )


    if len(content) > 2000:

        return error_response(
            "Le commentaire est trop long.",
            "CONTENT_TOO_LONG",
            400
        )


    comment.content = content

    db.session.commit()


    return success_response(

        "Commentaire modifié avec succès.",

        {
            "comment":
                comment.to_dict()
        }

    )


# ==================================
# DELETE COMMENT
# ==================================

@comments_bp.delete(
    "/<int:comment_id>"
)
@jwt_required()
def delete_comment(
    comment_id
):

    user_id = get_jwt_identity()

    comment = Comment.query.get(
        comment_id
    )


    if not comment:

        return error_response(
            "Commentaire introuvable.",
            "COMMENT_NOT_FOUND",
            404
        )


    if comment.user_id != int(
        user_id
    ):

        return error_response(
            "Vous ne pouvez supprimer que votre propre commentaire.",
            "FORBIDDEN",
            403
        )


    db.session.delete(
        comment
    )

    db.session.commit()


    return success_response(

        "Commentaire supprimé avec succès.",

        None

    )


# ==================================
# REPORT COMMENT
# ==================================

@comments_bp.patch(
    "/<int:comment_id>/report"
)
@jwt_required()
def report_comment(
    comment_id
):

    comment = Comment.query.get(
        comment_id
    )


    if not comment:

        return error_response(
            "Commentaire introuvable.",
            "COMMENT_NOT_FOUND",
            404
        )


    if comment.status == "reported":

        return success_response(
            "Ce commentaire a déjà été signalé.",
            {
                "comment_id":
                    comment.id
            }
        )


    comment.status = "reported"

    db.session.commit()


    return success_response(

        "Commentaire signalé.",

        {
            "comment_id":
                comment.id
        }

    )
    
    # ==================================
# REGISTER BLUEPRINT
# ==================================

def register_comment_routes(app):

    app.register_blueprint(
        comments_bp
    )

    return app