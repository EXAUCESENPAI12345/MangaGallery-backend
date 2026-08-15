from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db
from models.chapter import Chapter
from models.manga import Manga
from utils.authz import require_admin

chapters_bp = Blueprint("chapters", __name__)

@chapters_bp.get("/")
def get_chapters():
    manga_id = request.args.get("manga_id", type=int)
    query = Chapter.query
    if manga_id is not None: query = query.filter_by(manga_id=manga_id)
    return jsonify([c.to_dict() for c in query.order_by(Chapter.manga_id, Chapter.number).all()])

@chapters_bp.get("/<int:chapter_id>")
def get_chapter(chapter_id):
    c = Chapter.query.get(chapter_id)
    if not c: return jsonify(success=False, message="Chapitre introuvable"), 404
    if c.visibility != "public": return jsonify(success=False, message="Chapitre indisponible"), 404
    return jsonify(c.to_dict())

@chapters_bp.get("/search")
def search_chapter():
    q = request.args.get("q", "").strip()
    query = Chapter.query
    if q: query = query.filter(Chapter.title.ilike(f"%{q}%"))
    return jsonify([c.to_dict() for c in query.order_by(Chapter.number).all()])

@chapters_bp.post("/")
@require_admin
def create_chapter():
    data = request.get_json(silent=True) or {}
    manga_id = data.get("manga_id"); number = data.get("number")
    if manga_id is None or number is None: return jsonify(success=False, message="manga_id et number sont obligatoires"), 400
    try: manga_id = int(manga_id); number = float(number)
    except (TypeError, ValueError): return jsonify(success=False, message="Données de chapitre invalides"), 400
    if not Manga.query.get(manga_id): return jsonify(success=False, message="Manga introuvable"), 404
    if number < 0: return jsonify(success=False, message="Numéro de chapitre invalide"), 400
    if Chapter.query.filter_by(manga_id=manga_id, number=number).first(): return jsonify(success=False, message="Ce chapitre existe déjà"), 409
    slug = str(data.get("slug") or f"chapter-{str(number).replace('.', '-')}").strip().lower()
    c = Chapter(manga_id=manga_id, number=number, title=str(data.get("title") or "").strip() or None, slug=slug, pages=data.get("pages") or [], status=data.get("status", "published"), visibility=data.get("visibility", "public"), published_at=datetime.utcnow() if data.get("published", True) else None)
    db.session.add(c); db.session.commit()
    return jsonify(success=True, message="Chapitre créé", chapter=c.to_dict()), 201

@chapters_bp.put("/<int:chapter_id>")
@require_admin
def update_chapter(chapter_id):
    c = Chapter.query.get(chapter_id)
    if not c: return jsonify(success=False, message="Chapitre introuvable"), 404
    data = request.get_json(silent=True) or {}
    for field in ("number", "title", "slug", "pages", "status", "visibility", "published_at"):
        if field in data: setattr(c, field, data[field])
    db.session.commit(); return jsonify(success=True, message="Chapitre mis à jour", chapter=c.to_dict())

@chapters_bp.delete("/<int:chapter_id>")
@require_admin
def delete_chapter(chapter_id):
    c = Chapter.query.get(chapter_id)
    if not c: return jsonify(success=False, message="Chapitre introuvable"), 404
    db.session.delete(c); db.session.commit(); return jsonify(success=True, message="Chapitre supprimé")

@chapters_bp.post("/<int:chapter_id>/pages")
@require_admin
def upload_pages(chapter_id):
    c = Chapter.query.get(chapter_id)
    if not c: return jsonify(success=False, message="Chapitre introuvable"), 404
    data = request.get_json(silent=True) or {}
    pages = data.get("pages")
    if not isinstance(pages, list): return jsonify(success=False, message="pages doit être une liste"), 400
    c.pages = pages; db.session.commit(); return jsonify(success=True, message="Pages mises à jour", chapter=c.to_dict())

@chapters_bp.get("/<int:chapter_id>/read")
def read_chapter(chapter_id):
    c = Chapter.query.get(chapter_id)
    if not c or c.visibility != "public": return jsonify(success=False, message="Chapitre introuvable"), 404
    return jsonify(success=True, chapter=c.to_dict())

@chapters_bp.patch("/<int:chapter_id>/views")
@require_admin
def update_views(chapter_id):
    c = Chapter.query.get(chapter_id)
    if not c: return jsonify(success=False, message="Chapitre introuvable"), 404
    return jsonify(success=True, message="Aucun compteur de vues n'est défini sur le modèle Chapter")

@chapters_bp.get("/status")
def status(): return jsonify(service="Chapters", status="online")
