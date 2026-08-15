from flask import Blueprint, request, jsonify
from database import db
from models.role import Role
from models.user import User
from utils.authz import require_admin

roles_bp=Blueprint("roles",__name__)

@roles_bp.get("/")
@require_admin
def get_roles():return jsonify([r.to_dict() for r in Role.query.order_by(Role.id).all()])

@roles_bp.get("/<int:role_id>")
@require_admin
def get_role(role_id):
 r=Role.query.get(role_id)
 if not r:return jsonify(success=False,message="Rôle introuvable"),404
 return jsonify(r.to_dict())

@roles_bp.get("/search")
@require_admin
def search_role():
 q=request.args.get("q","").strip();query=Role.query
 if q:query=query.filter(Role.name.ilike(f"%{q}%"))
 return jsonify([r.to_dict() for r in query.all()])

@roles_bp.post("/")
@require_admin
def create_role():
 data=request.get_json(silent=True) or {};name=str(data.get("name","")).strip()
 if not name:return jsonify(success=False,message="name obligatoire"),400
 if name=="admin" or Role.query.filter_by(name=name).first():return jsonify(success=False,message="Le rôle admin est unique et les autres rôles doivent avoir un nom différent"),409
 r=Role(name=name,description=data.get("description"),permissions=data.get("permissions") or {},is_system=False,is_active=True);db.session.add(r);db.session.commit();return jsonify(success=True,role=r.to_dict()),201

@roles_bp.put("/<int:role_id>")
@require_admin
def update_role(role_id):
 r=Role.query.get(role_id)
 if not r:return jsonify(success=False,message="Rôle introuvable"),404
 data=request.get_json(silent=True) or {}
 if r.name=="admin" and data.get("name") not in (None,"admin"):return jsonify(success=False,message="Le rôle admin ne peut pas être renommé"),403
 for f in ("name","description","permissions","is_active"):
  if f in data:setattr(r,f,data[f])
 db.session.commit();return jsonify(success=True,role=r.to_dict())

@roles_bp.delete("/<int:role_id>")
@require_admin
def delete_role(role_id):
 r=Role.query.get(role_id)
 if not r:return jsonify(success=False,message="Rôle introuvable"),404
 if r.name=="admin" or r.is_system:return jsonify(success=False,message="Le rôle système admin ne peut pas être supprimé"),403
 db.session.delete(r);db.session.commit();return jsonify(success=True,message="Rôle supprimé")

@roles_bp.patch("/<int:user_id>/assign")
@require_admin
def assign_role(user_id):
 u=User.query.get(user_id);data=request.get_json(silent=True) or {};name=str(data.get("role","user"))
 if not u:return jsonify(success=False,message="Utilisateur introuvable"),404
 if name=="admin":return jsonify(success=False,message="Exauce est le seul administrateur"),403
 r=Role.query.filter_by(name=name).first()
 u.role=name;u.role_id=r.id if r else None;db.session.commit();return jsonify(success=True,user=u.to_dict())

@roles_bp.patch("/<int:role_id>/permissions")
@require_admin
def update_permissions(role_id):
 r=Role.query.get(role_id)
 if not r:return jsonify(success=False,message="Rôle introuvable"),404
 r.permissions=(request.get_json(silent=True) or {}).get("permissions") or {};db.session.commit();return jsonify(success=True,role=r.to_dict())

@roles_bp.get("/status")
def status():return jsonify(service="Roles",status="online")
