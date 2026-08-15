from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db
from models.notification import Notification
from models.user import User
from utils.authz import require_admin

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.get("/")
@require_admin
def get_notifications(): return jsonify([n.to_dict() for n in Notification.query.order_by(Notification.created_at.desc()).all()])

@notifications_bp.get("user/<int:user_id>")
@require_admin
def get_user_notifications(user_id):
    if not User.query.get(user_id): return jsonify(success=False, message="Utilisateur introuvable"), 404
    return jsonify([n.to_dict() for n in Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()])

@notifications_bp.get("/<int:notification_id>")
@require_admin
def get_notification(notification_id):
    n=Notification.query.get(notification_id)
    if not n: return jsonify(success=False, message="Notification introuvable"),404
    return jsonify(n.to_dict())

@notifications_bp.post("/")
@require_admin
def send_notification():
    data=request.get_json(silent=True) or {}; title=str(data.get("title","")).strip(); message=str(data.get("message","")).strip()
    if not title or not message: return jsonify(success=False,message="title et message sont obligatoires"),400
    uid=data.get("user_id")
    if uid is not None and not User.query.get(uid): return jsonify(success=False,message="Utilisateur introuvable"),404
    n=Notification(user_id=uid,title=title,message=message,type=data.get("type","system"),data=data.get("data") or {})
    db.session.add(n);db.session.commit();return jsonify(success=True,message="Notification créée",notification=n.to_dict()),201

@notifications_bp.post("/broadcast")
@require_admin
def broadcast_notification():
    data=request.get_json(silent=True) or {}; title=str(data.get("title","")).strip(); message=str(data.get("message","")).strip()
    if not title or not message:return jsonify(success=False,message="title et message sont obligatoires"),400
    users=User.query.filter_by(status="active").all()
    for u in users: db.session.add(Notification(user_id=u.id,title=title,message=message,type=data.get("type","system"),data=data.get("data") or {}))
    db.session.commit();return jsonify(success=True,message="Notification diffusée",recipients=len(users)),201

@notifications_bp.patch("/<int:notification_id>/read")
@require_admin
def mark_as_read(notification_id):
    n=Notification.query.get(notification_id)
    if not n:return jsonify(success=False,message="Notification introuvable"),404
    n.mark_as_read();db.session.commit();return jsonify(success=True,notification=n.to_dict())

@notifications_bp.delete("/<int:notification_id>")
@require_admin
def delete_notification(notification_id):
    n=Notification.query.get(notification_id)
    if not n:return jsonify(success=False,message="Notification introuvable"),404
    db.session.delete(n);db.session.commit();return jsonify(success=True,message="Notification supprimée")

@notifications_bp.get("/statistics")
@require_admin
def notification_statistics():
    total=Notification.query.count(); unread=Notification.query.filter_by(is_read=False).count()
    return jsonify(success=True,statistics={"total":total,"unread":unread,"read":total-unread})

@notifications_bp.get("/status")
def status():return jsonify(service="Notifications",status="online")
