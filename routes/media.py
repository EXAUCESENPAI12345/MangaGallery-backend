import os
from flask import Blueprint, request, jsonify, send_file
from database import db
from models.media import Media
from utils.authz import require_admin
from utils.file_upload import allowed_file, save_file, validate_file_size, delete_file

media_bp=Blueprint("media",__name__)
UPLOAD_DIR=os.getenv("MEDIA_UPLOAD_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads"))

@media_bp.get("/")
@require_admin
def get_media(): return jsonify([m.to_dict() for m in Media.query.order_by(Media.created_at.desc()).all()])

@media_bp.get("/<int:media_id>")
@require_admin
def get_one_media(media_id):
 m=Media.query.get(media_id)
 if not m:return jsonify(success=False,message="Média introuvable"),404
 return jsonify(m.to_dict())

@media_bp.get("/search")
@require_admin
def search_media():
 q=request.args.get("q","").strip();query=Media.query
 if q:query=query.filter((Media.filename.ilike(f"%{q}%")) | (Media.original_name.ilike(f"%{q}%")))
 return jsonify([m.to_dict() for m in query.order_by(Media.created_at.desc()).all()])

@media_bp.post("/upload")
@require_admin
def upload_media():
 f=request.files.get("file")
 if not f or not f.filename:return jsonify(success=False,message="Fichier obligatoire"),400
 if not allowed_file(f.filename):return jsonify(success=False,message="Type de fichier non autorisé"),400
 if not validate_file_size(f):return jsonify(success=False,message="Fichier trop volumineux"),413
 path=save_file(f,UPLOAD_DIR); relative=os.path.relpath(path,UPLOAD_DIR)
 m=Media(manga_id=request.form.get("manga_id",type=int),chapter_id=request.form.get("chapter_id",type=int),filename=os.path.basename(path),original_name=f.filename,file_type=f.filename.rsplit('.',1)[1].lower(),mime_type=f.mimetype,file_size=os.path.getsize(path),file_path=path)
 db.session.add(m);db.session.commit();return jsonify(success=True,message="Fichier envoyé",media=m.to_dict()),201

@media_bp.patch("/<int:media_id>/rename")
@require_admin
def rename_media(media_id):
 m=Media.query.get(media_id)
 if not m:return jsonify(success=False,message="Média introuvable"),404
 name=str((request.get_json(silent=True) or {}).get("original_name","")).strip()
 if not name:return jsonify(success=False,message="original_name obligatoire"),400
 m.original_name=name;db.session.commit();return jsonify(success=True,media=m.to_dict())

@media_bp.get("/<int:media_id>/download")
@require_admin
def download_media(media_id):
 m=Media.query.get(media_id)
 if not m or not os.path.isfile(m.file_path):return jsonify(success=False,message="Fichier introuvable"),404
 return send_file(m.file_path,as_attachment=True,download_name=m.original_name)

@media_bp.delete("/<int:media_id>")
@require_admin
def delete_media(media_id):
 m=Media.query.get(media_id)
 if not m:return jsonify(success=False,message="Média introuvable"),404
 delete_file(m.file_path);db.session.delete(m);db.session.commit();return jsonify(success=True,message="Fichier supprimé")

@media_bp.get("/statistics")
@require_admin
def media_statistics():
 items=Media.query.all();return jsonify(success=True,statistics={"total":len(items),"size_bytes":sum(int(m.file_size or 0) for m in items)})

@media_bp.get("/status")
def status():return jsonify(service="Media",status="online")
