from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from database import db
from models.user import User
from models.role import Role
from utils.authz import require_admin

users_bp = Blueprint("users", __name__)

@users_bp.get("/")
@require_admin
def get_users(): return jsonify([u.to_dict() for u in User.query.order_by(User.id).all()])

@users_bp.get("/<int:user_id>")
@require_admin
def get_user(user_id):
    u = User.query.get(user_id)
    if not u: return jsonify(success=False, message="Utilisateur introuvable"), 404
    return jsonify(u.to_dict())

@users_bp.get("/search")
@require_admin
def search_user():
    q = request.args.get("q", "").strip()
    query = User.query
    if q: query = query.filter((User.username.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%")))
    return jsonify([u.to_dict() for u in query.order_by(User.id).all()])

@users_bp.post("/")
@require_admin
def create_user():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username") or "").strip() or None
    email = str(data.get("email") or "").strip() or None
    if email and User.query.filter_by(email=email).first(): return jsonify(success=False, message="Email déjà utilisé"), 409
    if username and User.query.filter_by(username=username).first(): return jsonify(success=False, message="Nom d'utilisateur déjà utilisé"), 409
    role_name = str(data.get("role", "user"))
    if role_name == "admin": return jsonify(success=False, message="Le seul administrateur est Exauce"), 403
    u = User(telegram_id=data.get("telegram_id"), username=username, first_name=data.get("first_name"), last_name=data.get("last_name"), photo_url=data.get("photo_url"), email=email, password_hash=generate_password_hash(str(data["password"])) if data.get("password") else None, role="user", role_id=None, status=data.get("status", "active"), is_verified=bool(data.get("is_verified", False)))
    db.session.add(u); db.session.commit(); return jsonify(success=True, message="Utilisateur créé", user=u.to_dict()), 201

@users_bp.put("/<int:user_id>")
@require_admin
def update_user(user_id):
    u = User.query.get(user_id)
    if not u: return jsonify(success=False, message="Utilisateur introuvable"), 404
    data = request.get_json(silent=True) or {}
    for field in ("username", "first_name", "last_name", "photo_url", "email", "status", "is_verified"):
        if field in data: setattr(u, field, data[field])
    if "password" in data and data["password"]: u.password_hash = generate_password_hash(str(data["password"]))
    db.session.commit(); return jsonify(success=True, message="Utilisateur mis à jour", user=u.to_dict())

@users_bp.delete("/<int:user_id>")
@require_admin
def delete_user(user_id):
    u = User.query.get(user_id)
    if not u: return jsonify(success=False, message="Utilisateur introuvable"), 404
    if u.id == 1 or u.role == "admin": return jsonify(success=False, message="Le compte administrateur Exauce ne peut pas être supprimé"), 403
    db.session.delete(u); db.session.commit(); return jsonify(success=True, message="Utilisateur supprimé")

@users_bp.patch("/<int:user_id>/status")
@require_admin
def update_user_status(user_id):
    u = User.query.get(user_id)
    if not u: return jsonify(success=False, message="Utilisateur introuvable"), 404
    if u.id == 1: return jsonify(success=False, message="Le compte administrateur ne peut pas être désactivé"), 403
    status = (request.get_json(silent=True) or {}).get("status")
    if status not in ("active", "inactive", "suspended"): return jsonify(success=False, message="Statut invalide"), 400
    u.status = status; db.session.commit(); return jsonify(success=True, user=u.to_dict())

@users_bp.patch("/<int:user_id>/role")
@require_admin
def update_user_role(user_id):
    u = User.query.get(user_id)
    if not u: return jsonify(success=False, message="Utilisateur introuvable"), 404
    role_name = str((request.get_json(silent=True) or {}).get("role", "user"))
    if role_name == "admin": return jsonify(success=False, message="Aucun autre administrateur ne peut être créé"), 403
    u.role = "user"; u.role_id = None; db.session.commit(); return jsonify(success=True, message="Rôle utilisateur mis à jour", user=u.to_dict())

@users_bp.get("/status")
def status(): return jsonify(service="Users", status="online")
