from flask import Blueprint, request, jsonify
from database import db
from models.category import Category
from utils.authz import require_admin

categories_bp = Blueprint("categories", __name__)

@categories_bp.get("/")
def get_categories():
    return jsonify([c.to_dict() for c in Category.query.order_by(Category.name.asc()).all()])

@categories_bp.get("/<int:category_id>")
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify(success=False, message="Catégorie introuvable"), 404
    return jsonify(category.to_dict())

@categories_bp.get("/search")
def search_category():
    q = request.args.get("q", "").strip()
    query = Category.query
    if q:
        query = query.filter(Category.name.ilike(f"%{q}%"))
    return jsonify([c.to_dict() for c in query.order_by(Category.name.asc()).all()])

@categories_bp.post("/")
@require_admin
def create_category():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify(success=False, message="Le nom est obligatoire"), 400
    slug = str(data.get("slug") or name.lower().replace(" ", "-")).strip()
    if Category.query.filter((Category.name == name) | (Category.slug == slug)).first():
        return jsonify(success=False, message="Cette catégorie existe déjà"), 409
    category = Category(name=name, slug=slug, description=data.get("description"), icon=data.get("icon"), color=data.get("color", "#E11D2E"), is_active=bool(data.get("is_active", True)))
    db.session.add(category); db.session.commit()
    return jsonify(success=True, message="Catégorie créée", category=category.to_dict()), 201

@categories_bp.put("/<int:category_id>")
@require_admin
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category: return jsonify(success=False, message="Catégorie introuvable"), 404
    data = request.get_json(silent=True) or {}
    for field in ("name", "slug", "description", "icon", "color", "is_active"):
        if field in data: setattr(category, field, data[field])
    db.session.commit()
    return jsonify(success=True, message="Catégorie mise à jour", category=category.to_dict())

@categories_bp.delete("/<int:category_id>")
@require_admin
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category: return jsonify(success=False, message="Catégorie introuvable"), 404
    db.session.delete(category); db.session.commit()
    return jsonify(success=True, message="Catégorie supprimée")

@categories_bp.get("/statistics")
@require_admin
def category_statistics():
    categories = Category.query.all()
    return jsonify(success=True, statistics={"total": len(categories), "active": sum(bool(c.is_active) for c in categories), "items": [{"id": c.id, "name": c.name, "mangas": len(c.mangas)} for c in categories]})

@categories_bp.get("/count")
def category_count():
    return jsonify(success=True, total_categories=Category.query.count())

@categories_bp.get("/status")
def status():
    return jsonify(service="Categories", status="online")
