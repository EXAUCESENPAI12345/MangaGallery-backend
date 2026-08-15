from flask import Blueprint, request, jsonify
from database import db
from models.manga import Manga
from models.category import Category
from utils.authz import require_admin, current_user

mangas_bp = Blueprint("mangas", __name__)

@mangas_bp.get("/")
def _invalid():
    return jsonify([])

@mangas_bp.get("/<int:manga_id>")
def get_manga(manga_id):
    manga = Manga.query.get(manga_id)
    if not manga: return jsonify(success=False, message="Manga introuvable"), 404
    return jsonify(manga.to_dict())

@mangas_bp.get("/search")
def search_manga():
    q = request.args.get("q", "").strip()
    query = Manga.query
    if q: query = query.filter(Manga.title.ilike(f"%{q}%"))
    return jsonify([m.to_dict() for m in query.order_by(Manga.title.asc()).all()])

@mangas_bp.post("/")
@require_admin
def create_manga():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title: return jsonify(success=False, message="Le titre est obligatoire"), 400
    slug = str(data.get("slug") or title.lower().replace(" ", "-")).strip()
    if Manga.query.filter_by(slug=slug).first(): return jsonify(success=False, message="Le slug existe déjà"), 409
    category_id = data.get("category_id")
    if category_id is not None and not Category.query.get(category_id): return jsonify(success=False, message="Catégorie introuvable"), 400
    user = current_user()
    manga = Manga(title=title, slug=slug, description=data.get("description"), cover_url=data.get("cover_url"), banner_url=data.get("banner_url"), status=data.get("status", "ongoing"), visibility=data.get("visibility", "public"), author_id=user.id if user else None, category_id=category_id)
    db.session.add(manga); db.session.commit()
    return jsonify(success=True, message="Manga créé", manga=manga.to_dict()), 201

@mangas_bp.put("/<int:manga_id>")
@require_admin
def update_manga(manga_id):
    manga = Manga.query.get(manga_id)
    if not manga: return jsonify(success=False, message="Manga introuvable"), 404
    data = request.get_json(silent=True) or {}
    for field in ("title", "slug", "description", "cover_url", "banner_url", "status", "visibility", "category_id"):
        if field in data: setattr(manga, field, data[field])
    db.session.commit()
    return jsonify(success=True, message="Manga mis à jour", manga=manga.to_dict())

@mangas_bp.delete("/<int:manga_id>")
@require_admin
def delete_manga(manga_id):
    manga = Manga.query.get(manga_id)
    if not manga: return jsonify(success=False, message="Manga introuvable"), 404
    db.session.delete(manga); db.session.commit()
    return jsonify(success=True, message="Manga supprimé")

@mangas_bp.patch("/<int:manga_id>/stats")
@require_admin
def update_manga_stats(manga_id):
    manga = Manga.query.get(manga_id)
    if not manga: return jsonify(success=False, message="Manga introuvable"), 404
    return jsonify(success=True, message="Aucune statistique persistante n'est définie sur le modèle Manga", manga=manga.to_dict())

@mangas_bp.post("/<int:manga_id>/cover")
@require_admin
def upload_cover(manga_id):
    manga = Manga.query.get(manga_id)
    if not manga: return jsonify(success=False, message="Manga introuvable"), 404
    url = request.form.get("cover_url") or (request.get_json(silent=True) or {}).get("cover_url")
    if not url: return jsonify(success=False, message="cover_url obligatoire"), 400
    manga.cover_url = url; db.session.commit()
    return jsonify(success=True, message="Couverture mise à jour", manga=manga.to_dict())

@mangas_bp.post("/<int:manga_id>/banner")
@require_admin
def upload_banner(manga_id):
    manga = Manga.query.get(manga_id)
    if not manga: return jsonify(success=False, message="Manga introuvable"), 404
    url = request.form.get("banner_url") or (request.get_json(silent=True) or {}).get("banner_url")
    if not url: return jsonify(success=False, message="banner_url obligatoire"), 400
    manga.banner_url = url; db.session.commit()
    return jsonify(success=True, message="Bannière mise à jour", manga=manga.to_dict())

@mangas_bp.get("/status")
def status(): return jsonify(service="Mangas", status="online")
