from datetime import datetime

from flask import Blueprint, request

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from database import db
from models.chapter import Chapter
from models.manga import Manga


chapters_bp = Blueprint(
    "chapters",
    __name__,
    url_prefix="/api/chapters"
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
# LIST CHAPTERS
# ==================================

@chapters_bp.get("")
def list_chapters():

    manga_id = request.args.get(
        "manga_id",
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


    query = Chapter.query.filter(
        Chapter.visibility == "public"
    )


    if manga_id:

        query = query.filter(
            Chapter.manga_id == manga_id
        )


    pagination = query.order_by(
        Chapter.number.desc()
    ).paginate(

        page=page,

        per_page=per_page,

        error_out=False

    )


    return success_response(

        "Chapitres récupérés.",

        {

            "items": [

                chapter.to_dict()

                for chapter
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
# GET CHAPTER
# ==================================

@chapters_bp.get(
    "/<int:chapter_id>"
)
def get_chapter(
    chapter_id
):

    chapter = Chapter.query.get(
        chapter_id
    )


    if not chapter:

        return error_response(
            "Chapitre introuvable.",
            "CHAPTER_NOT_FOUND",
            404
        )


    if chapter.visibility != "public":

        return error_response(
            "Chapitre indisponible.",
            "CHAPTER_UNAVAILABLE",
            404
        )


    return success_response(

        "Chapitre récupéré.",

        {
            "chapter":
                chapter.to_dict()
        }

    )


# ==================================
# CREATE CHAPTER
# ==================================

@chapters_bp.post("")
@jwt_required()
def create_chapter():

    data = request.get_json(
        silent=True
    ) or {}


    manga_id = data.get(
        "manga_id"
    )

    number = data.get(
        "number"
    )


    if manga_id is None:

        return error_response(
            "L'identifiant du manga est obligatoire.",
            "MANGA_ID_REQUIRED",
            400
        )


    if number is None:

        return error_response(
            "Le numéro du chapitre est obligatoire.",
            "CHAPTER_NUMBER_REQUIRED",
            400
        )


    try:

        manga_id = int(
            manga_id
        )

        number = float(
            number
        )

    except (
        TypeError,
        ValueError
    ):

        return error_response(
            "Identifiant ou numéro de chapitre invalide.",
            "INVALID_CHAPTER_DATA",
            400
        )


    manga = Manga.query.get(
        manga_id
    )


    if not manga:

        return error_response(
            "Manga introuvable.",
            "MANGA_NOT_FOUND",
            404
        )


    if number < 0:

        return error_response(
            "Le numéro du chapitre est invalide.",
            "INVALID_CHAPTER_NUMBER",
            400
        )


    existing = Chapter.query.filter(
        Chapter.manga_id == manga_id,
        Chapter.number == number
    ).first()


    if existing:

        return error_response(
            "Ce chapitre existe déjà pour ce manga.",
            "CHAPTER_EXISTS",
            409
        )


    slug = str(
        data.get(
            "slug",
            f"chapter-{str(number).replace('.', '-')}"
        )
    ).strip().lower()


    chapter = Chapter(

        manga_id=manga_id,

        number=number,

        title=str(
            data.get(
                "title",
                ""
            )
        ).strip() or None,

        slug=slug,

        pages=data.get(
            "pages",
            []
        ),

        status=data.get(
            "status",
            "published"
        ),

        visibility=data.get(
            "visibility",
            "public"
        ),

        published_at=datetime.utcnow()

    )


    db.session.add(
        chapter
    )

    db.session.commit()


    return success_response(

        "Chapitre créé avec succès.",

        {
            "chapter":
                chapter.to_dict()
        },

        201

    )
    
    # ==================================
# UPDATE CHAPTER
# ==================================

@chapters_bp.put(
    "/<int:chapter_id>"
)
@jwt_required()
def update_chapter(
    chapter_id
):

    chapter = Chapter.query.get(
        chapter_id
    )

    if not chapter:

        return error_response(
            "Chapitre introuvable.",
            "CHAPTER_NOT_FOUND",
            404
        )


    data = request.get_json(
        silent=True
    ) or {}


    if "number" in data:

        try:

            number = float(
                data.get(
                    "number"
                )
            )

        except (
            TypeError,
            ValueError
        ):

            return error_response(
                "Numéro de chapitre invalide.",
                "INVALID_CHAPTER_NUMBER",
                400
            )


        if number < 0:

            return error_response(
                "Le numéro du chapitre est invalide.",
                "INVALID_CHAPTER_NUMBER",
                400
            )


        existing = Chapter.query.filter(

            Chapter.manga_id ==
                chapter.manga_id,

            Chapter.number ==
                number,

            Chapter.id !=
                chapter.id

        ).first()


        if existing:

            return error_response(
                "Ce numéro de chapitre existe déjà.",
                "CHAPTER_EXISTS",
                409
            )


        chapter.number = number


    if "title" in data:

        chapter.title = (

            str(
                data.get(
                    "title"
                )
            ).strip()

            or None

        )


    if "slug" in data:

        slug = str(
            data.get(
                "slug"
            )
        ).strip().lower()


        if not slug:

            return error_response(
                "Le slug ne peut pas être vide.",
                "INVALID_SLUG",
                400
            )


        chapter.slug = slug


    if "pages" in data:

        pages = data.get(
            "pages"
        )


        if not isinstance(
            pages,
            list
        ):

            return error_response(
                "Les pages doivent être une liste.",
                "INVALID_PAGES",
                400
            )


        chapter.pages = pages


    if "status" in data:

        allowed_statuses = {

            "draft",
            "published",
            "archived"

        }


        status = str(
            data.get(
                "status"
            )
        ).strip().lower()


        if status not in allowed_statuses:

            return error_response(
                "Statut du chapitre invalide.",
                "INVALID_STATUS",
                400
            )


        chapter.status = status


    if "visibility" in data:

        allowed_visibility = {

            "public",
            "private"

        }


        visibility = str(
            data.get(
                "visibility"
            )
        ).strip().lower()


        if visibility not in allowed_visibility:

            return error_response(
                "Visibilité invalide.",
                "INVALID_VISIBILITY",
                400
            )


        chapter.visibility = visibility


    if "published_at" in data:

        published_at = data.get(
            "published_at"
        )

        if published_at:

            try:

                chapter.published_at = (
                    datetime.fromisoformat(
                        str(
                            published_at
                        ).replace(
                            "Z",
                            "+00:00"
                        )
                    )
                )

            except ValueError:

                return error_response(
                    "Date de publication invalide.",
                    "INVALID_DATE",
                    400
                )

        else:

            chapter.published_at = None


    db.session.commit()


    return success_response(

        "Chapitre mis à jour avec succès.",

        {
            "chapter":
                chapter.to_dict()
        }

    )


# ==================================
# DELETE CHAPTER
# ==================================

@chapters_bp.delete(
    "/<int:chapter_id>"
)
@jwt_required()
def delete_chapter(
    chapter_id
):

    chapter = Chapter.query.get(
        chapter_id
    )


    if not chapter:

        return error_response(
            "Chapitre introuvable.",
            "CHAPTER_NOT_FOUND",
            404
        )


    db.session.delete(
        chapter
    )

    db.session.commit()


    return success_response(

        "Chapitre supprimé avec succès.",

        None

    )
    
    # ==================================
# CHAPTER BY SLUG
# ==================================

@chapters_bp.get(
    "/slug/<string:slug>"
)
def get_chapter_by_slug(
    slug
):

    chapter = Chapter.query.filter(
        Chapter.slug == slug,
        Chapter.visibility == "public"
    ).first()


    if not chapter:

        return error_response(
            "Chapitre introuvable.",
            "CHAPTER_NOT_FOUND",
            404
        )


    return success_response(

        "Chapitre récupéré.",

        {
            "chapter":
                chapter.to_dict()
        }

    )


# ==================================
# CHAPTER PAGES
# ==================================

@chapters_bp.get(
    "/<int:chapter_id>/pages"
)
def get_chapter_pages(
    chapter_id
):

    chapter = Chapter.query.get(
        chapter_id
    )


    if not chapter:

        return error_response(
            "Chapitre introuvable.",
            "CHAPTER_NOT_FOUND",
            404
        )


    if chapter.visibility != "public":

        return error_response(
            "Chapitre indisponible.",
            "CHAPTER_UNAVAILABLE",
            404
        )


    return success_response(

        "Pages récupérées.",

        {

            "chapter_id":
                chapter.id,

            "pages":
                chapter.pages or [],

            "total":
                len(
                    chapter.pages or []
                )

        }

    )


# ==================================
# PUBLISH CHAPTER
# ==================================

@chapters_bp.patch(
    "/<int:chapter_id>/publish"
)
@jwt_required()
def publish_chapter(
    chapter_id
):

    chapter = Chapter.query.get(
        chapter_id
    )


    if not chapter:

        return error_response(
            "Chapitre introuvable.",
            "CHAPTER_NOT_FOUND",
            404
        )


    chapter.status = "published"

    chapter.visibility = "public"

    chapter.published_at = (
        datetime.utcnow()
    )


    db.session.commit()


    return success_response(

        "Chapitre publié avec succès.",

        {
            "chapter":
                chapter.to_dict()
        }

    )


# ==================================
# REGISTER BLUEPRINT
# ==================================

def register_chapter_routes(app):

    app.register_blueprint(
        chapters_bp
    )

    return app