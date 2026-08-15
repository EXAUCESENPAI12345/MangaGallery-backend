from flask import Blueprint, request

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from database import db
from models.manga import Manga


mangas_bp = Blueprint(
    "mangas",
    __name__,
    url_prefix="/api/mangas"
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
# LIST MANGAS
# ==================================

@mangas_bp.get("")
def list_mangas():

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

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()


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


    query = Manga.query.filter(
        Manga.visibility == "public"
    )


    if search:

        query = query.filter(
            Manga.title.ilike(
                f"%{search}%"
            )
        )


    pagination = query.order_by(
        Manga.updated_at.desc()
    ).paginate(

        page=page,

        per_page=per_page,

        error_out=False

    )


    return success_response(

        "Mangas récupérés.",

        {

            "items": [

                manga.to_dict()

                for manga
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
# GET MANGA
# ==================================

@mangas_bp.get(
    "/<int:manga_id>"
)
def get_manga(
    manga_id
):

    manga = Manga.query.get(
        manga_id
    )


    if not manga:

        return error_response(
            "Manga introuvable.",
            "MANGA_NOT_FOUND",
            404
        )


    if manga.visibility != "public":

        return error_response(
            "Manga indisponible.",
            "MANGA_UNAVAILABLE",
            404
        )


    return success_response(

        "Manga récupéré.",

        {
            "manga":
                manga.to_dict()
        }

    )


# ==================================
# CREATE MANGA
# ==================================

@mangas_bp.post("")
@jwt_required()
def create_manga():

    data = request.get_json(
        silent=True
    ) or {}


    title = str(
        data.get(
            "title",
            ""
        )
    ).strip()

    slug = str(
        data.get(
            "slug",
            ""
        )
    ).strip().lower()


    if not title:

        return error_response(
            "Le titre du manga est obligatoire.",
            "TITLE_REQUIRED",
            400
        )


    if not slug:

        return error_response(
            "Le slug du manga est obligatoire.",
            "SLUG_REQUIRED",
            400
        )


    existing = Manga.query.filter(
        Manga.slug == slug
    ).first()


    if existing:

        return error_response(
            "Ce slug existe déjà.",
            "SLUG_EXISTS",
            409
        )


    author_id = int(
        get_jwt_identity()
    )


    manga = Manga(

        title=title,

        slug=slug,

        description=str(
            data.get(
                "description",
                ""
            )
        ).strip() or None,

        cover_url=data.get(
            "cover_url"
        ),

        banner_url=data.get(
            "banner_url"
        ),

        status=data.get(
            "status",
            "ongoing"
        ),

        visibility=data.get(
            "visibility",
            "public"
        ),

        author_id=author_id

    )


    db.session.add(
        manga
    )

    db.session.commit()


    return success_response(

        "Manga créé avec succès.",

        {
            "manga":
                manga.to_dict()
        },

        201

    )
    
    # ==================================
# UPDATE MANGA
# ==================================

@mangas_bp.put(
    "/<int:manga_id>"
)
@jwt_required()
def update_manga(
    manga_id
):

    manga = Manga.query.get(
        manga_id
    )

    if not manga:

        return error_response(
            "Manga introuvable.",
            "MANGA_NOT_FOUND",
            404
        )


    data = request.get_json(
        silent=True
    ) or {}


    if "title" in data:

        title = str(
            data.get("title")
        ).strip()

        if not title:

            return error_response(
                "Le titre ne peut pas être vide.",
                "INVALID_TITLE",
                400
            )

        manga.title = title


    if "slug" in data:

        slug = str(
            data.get("slug")
        ).strip().lower()

        if not slug:

            return error_response(
                "Le slug ne peut pas être vide.",
                "INVALID_SLUG",
                400
            )


        existing = Manga.query.filter(
            Manga.slug == slug,
            Manga.id != manga.id
        ).first()


        if existing:

            return error_response(
                "Ce slug existe déjà.",
                "SLUG_EXISTS",
                409
            )


        manga.slug = slug


    if "description" in data:

        manga.description = (
            str(
                data.get(
                    "description"
                )
            ).strip()
            or None
        )


    if "cover_url" in data:

        manga.cover_url = (
            data.get(
                "cover_url"
            )
        )


    if "banner_url" in data:

        manga.banner_url = (
            data.get(
                "banner_url"
            )
        )


    if "status" in data:

        allowed_statuses = {

            "ongoing",
            "completed",
            "hiatus"

        }

        status = str(
            data.get("status")
        ).strip().lower()


        if status not in allowed_statuses:

            return error_response(
                "Statut du manga invalide.",
                "INVALID_STATUS",
                400
            )


        manga.status = status


    if "visibility" in data:

        allowed_visibility = {

            "public",
            "private"

        }

        visibility = str(
            data.get("visibility")
        ).strip().lower()


        if visibility not in allowed_visibility:

            return error_response(
                "Visibilité invalide.",
                "INVALID_VISIBILITY",
                400
            )


        manga.visibility = visibility


    db.session.commit()


    return success_response(

        "Manga mis à jour avec succès.",

        {
            "manga":
                manga.to_dict()
        }

    )


# ==================================
# DELETE MANGA
# ==================================

@mangas_bp.delete(
    "/<int:manga_id>"
)
@jwt_required()
def delete_manga(
    manga_id
):

    manga = Manga.query.get(
        manga_id
    )


    if not manga:

        return error_response(
            "Manga introuvable.",
            "MANGA_NOT_FOUND",
            404
        )


    db.session.delete(
        manga
    )

    db.session.commit()


    return success_response(

        "Manga supprimé avec succès.",

        None

    )


# ==================================
# MANGA CHAPTERS
# ==================================

@mangas_bp.get(
    "/<int:manga_id>/chapters"
)
def manga_chapters(
    manga_id
):

    manga = Manga.query.get(
        manga_id
    )


    if not manga:

        return error_response(
            "Manga introuvable.",
            "MANGA_NOT_FOUND",
            404
        )


    chapters = [

        chapter.to_dict()

        for chapter
        in manga.chapters

        if chapter.visibility == "public"

    ]


    return success_response(

        "Chapitres récupérés.",

        {
            "manga_id":
                manga.id,

            "items":
                chapters
        }

    )


# ==================================
# REGISTER BLUEPRINT
# ==================================

def register_manga_routes(app):

    app.register_blueprint(
        mangas_bp
    )

    return app
    
    
    # ==================================
# MANGA BY SLUG
# ==================================

@mangas_bp.get(
    "/slug/<string:slug>"
)
def get_manga_by_slug(
    slug
):

    manga = Manga.query.filter(
        Manga.slug == slug,
        Manga.visibility == "public"
    ).first()


    if not manga:

        return error_response(
            "Manga introuvable.",
            "MANGA_NOT_FOUND",
            404
        )


    return success_response(

        "Manga récupéré.",

        {
            "manga":
                manga.to_dict()
        }

    )


# ==================================
# SEARCH MANGAS
# ==================================

@mangas_bp.get(
    "/search"
)
def search_mangas():

    query_text = request.args.get(
        "q",
        "",
        type=str
    ).strip()


    if not query_text:

        return success_response(

            "Recherche effectuée.",

            {
                "items": []
            }

        )


    mangas = Manga.query.filter(

        Manga.visibility == "public",

        Manga.title.ilike(
            f"%{query_text}%"
        )

    ).order_by(

        Manga.title.asc()

    ).limit(50).all()


    return success_response(

        "Recherche effectuée.",

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
# REGISTER BLUEPRINT
# ==================================

def register_manga_routes(app):

    app.register_blueprint(
        mangas_bp
    )

    return app