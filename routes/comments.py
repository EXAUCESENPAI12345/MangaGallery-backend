from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from database import db
from models.comment import Comment
from models.manga import Manga
from models.chapter import Chapter
from utils.authz import require_admin, current_user

comments_bp = Blueprint("comments", __name__)

@comments_bp.get("/")
def get_comments():
    q = request.args.get("q", "").strip(); query = Comment.query
    if q: query = query.filter(Comment.content.ilike(f"%{q}%"))
    return jsonify([c.to_dict() for c in query.order_by(Comment.created_at.desc()).all()])

@comments_bp.get("/<int:comment_id>")
def get_comment(comment_id):
    c = Comment.query.get(comment_id)
    if not c: return jsonify(success=False, message="Commentaire introuvable"), 404
    return jsonify(c.to_dict())

@comments_bp.get("/search")
def search_comment():
    return get_comments()

@comments_bp.post("/")
@jwt_required()
def create_comment():
    data = request.get_json(silent=True) or {}; user = current_user()
    if not user: return jsonify(success=False, message="Utilisateur introuvable"), 401
    content = str(data.get("content", "")).strip()
    if not content: return jsonify(success=False, message="Le contenu est obligatoire"), 400
    if data.get("manga_id") and not Manga.query.get(data["manga_id"]): return jsonify(success=False, message="Manga introuvable"), 404
    if data.get("chapter_id") and not Chapter.query.get(data["chapter_id"]): return jsonify(success=False, message="Chapitre introuvable"), 404
    c = Comment(user_id=user.id, manga_id=data.get("manga_id"), chapter_id=data.get("chapter_id"), content=content, status="visible")
    db.session.add(c); db.session.commit(); return jsonify(success=True, message="Commentaire ajouté", comment=c.to_dict()), 201

@comments_bp.put("/<int:comment_id>")
@jwt_required()
def update_comment(comment_id):
    c = Comment.query.get(comment_id); user = current_user()
    if not c: return jsonify(success=False, message="Commentaire introuvable"), 404
    if not user or (c.user_id != user.id and user.role != "admin"): return jsonify(success=False, message="Accès refusé"), 403
    data = request.get_json(silent=True) or {}; content = str(data.get("content", "")).strip()
    if not content: return jsonify(success=False, message="Le contenu est obligatoire"), 400
    c.content = content; db.session.commit(); return jsonify(success=True, comment=c.to_dict())

@comments_bp.delete("/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id):
    c = Comment.query.get(comment_id); user = current_user()
    if not c: return jsonify(success=False, message="Commentaire introuvable"), 404
    if not user or (c.user_id != user.id and user.role != "admin"): return jsonify(success=False, message="Accès refusé"), 403
    db.session.delete(c); db.session.commit(); return jsonify(success=True, message="Commentaire supprimé")

@comments_bp.patch("/<int:comment_id>/like")
@jwt_required()
def like_comment(comment_id):
    c = Comment.query.get(comment_id)
    if not c: return jsonify(success=False, message="Commentaire introuvable"), 404
    return jsonify(success=True, message="Like enregistré", comment_id=comment_id)

@comments_bp.post("/<int:comment_id>/report")
@jwt_required()
def report_comment(comment_id):
    c = Comment.query.get(comment_id)
    if not c: return jsonify(success=False, message="Commentaire introuvable"), 404
    return jsonify(success=True, message="Signalement enregistré", comment_id=comment_id), 201

@comments_bp.patch("/<int:comment_id>/status")
@require_admin
def update_comment_status(comment_id):
    c = Comment.query.get(comment_id)
    if not c: return jsonify(success=False, message="Commentaire introuvable"), 404
    status = (request.get_json(silent=True) or {}).get("status")
    if status not in ("visible", "hidden", "deleted"): return jsonify(success=False, message="Statut invalide"), 400
    c.status = status; db.session.commit(); return jsonify(success=True, comment=c.to_dict())

@comments_bp.get("/status")
def status(): return jsonify(service="Comments", status="online")
