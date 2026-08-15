from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db
from models.report import Report
from models.comment import Comment
from models.manga import Manga
from utils.authz import require_admin, current_user
from flask_jwt_extended import jwt_required

reports_bp=Blueprint("reports",__name__)

@reports_bp.get("/")
@require_admin
def get_reports():return jsonify([r.to_dict() for r in Report.query.order_by(Report.created_at.desc()).all()])

@reports_bp.get("/<int:report_id>")
@require_admin
def get_report(report_id):
 r=Report.query.get(report_id)
 if not r:return jsonify(success=False,message="Signalement introuvable"),404
 return jsonify(r.to_dict())

@reports_bp.get("/search")
@require_admin
def search_report():
 status=request.args.get("status"); q=Report.query
 if status:q=q.filter_by(status=status)
 return jsonify([r.to_dict() for r in q.order_by(Report.created_at.desc()).all()])

@reports_bp.post("/")
@jwt_required()
def create_report():
 data=request.get_json(silent=True) or {}; user=current_user(); reason=str(data.get("reason","")).strip()
 if not user:return jsonify(success=False,message="Utilisateur introuvable"),401
 if not reason:return jsonify(success=False,message="reason obligatoire"),400
 if data.get("manga_id") and not Manga.query.get(data["manga_id"]):return jsonify(success=False,message="Manga introuvable"),404
 if data.get("comment_id") and not Comment.query.get(data["comment_id"]):return jsonify(success=False,message="Commentaire introuvable"),404
 r=Report(user_id=user.id,manga_id=data.get("manga_id"),comment_id=data.get("comment_id"),reason=reason,status="pending")
 db.session.add(r);db.session.commit();return jsonify(success=True,message="Signalement créé",report=r.to_dict()),201

@reports_bp.patch("/<int:report_id>/approve")
@require_admin
def approve_report(report_id):
 r=Report.query.get(report_id)
 if not r:return jsonify(success=False,message="Signalement introuvable"),404
 u=current_user();r.status="approved";r.moderator_id=u.id;r.resolved_at=datetime.utcnow();r.moderator_note=(request.get_json(silent=True) or {}).get("note");db.session.commit();return jsonify(success=True,report=r.to_dict())

@reports_bp.patch("/<int:report_id>/reject")
@require_admin
def reject_report(report_id):
 r=Report.query.get(report_id)
 if not r:return jsonify(success=False,message="Signalement introuvable"),404
 u=current_user();r.status="rejected";r.moderator_id=u.id;r.resolved_at=datetime.utcnow();r.moderator_note=(request.get_json(silent=True) or {}).get("note");db.session.commit();return jsonify(success=True,report=r.to_dict())

@reports_bp.delete("/<int:report_id>")
@require_admin
def delete_report(report_id):
 r=Report.query.get(report_id)
 if not r:return jsonify(success=False,message="Signalement introuvable"),404
 db.session.delete(r);db.session.commit();return jsonify(success=True,message="Signalement supprimé")

@reports_bp.get("/statistics")
@require_admin
def report_statistics():
 return jsonify(success=True,statistics={"total":Report.query.count(),"pending":Report.query.filter_by(status="pending").count(),"approved":Report.query.filter_by(status="approved").count(),"rejected":Report.query.filter_by(status="rejected").count()})

@reports_bp.get("/count")
@require_admin
def report_count():return jsonify(success=True,total_reports=Report.query.count())

@reports_bp.get("/status")
def status():return jsonify(service="Reports",status="online")
