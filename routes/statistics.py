"""
==================================
MANGA GALLERY
STATISTICS ROUTES
==================================
"""

from flask import Blueprint, jsonify

from models.user import User
from models.manga import Manga
from models.chapter import Chapter
from models.category import Category
from models.comment import Comment


statistics_bp = Blueprint(
    "statistics",
    __name__
)


@statistics_bp.get("/")
def statistics():
    """Retourne les statistiques générales de l'application."""

    return jsonify({
        "success": True,
        "statistics": {
            "users": User.query.count(),
            "mangas": Manga.query.count(),
            "chapters": Chapter.query.count(),
            "categories": Category.query.count(),
            "comments": Comment.query.count()
        }
    }), 200


@statistics_bp.get("/summary")
def summary():
    """Résumé des statistiques principales."""

    return jsonify({
        "success": True,
        "users": User.query.count(),
        "mangas": Manga.query.count(),
        "chapters": Chapter.query.count(),
        "categories": Category.query.count(),
        "comments": Comment.query.count()
    }), 200
