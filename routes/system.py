import os, shutil, time
from flask import Blueprint, jsonify
from database import db
from config import Config
from utils.authz import require_admin

system_bp=Blueprint("system",__name__)
START_TIME=time.time()

@system_bp.get("/info")
@require_admin
def system_info():return jsonify(success=True,system={"application":Config.APP_NAME,"version":Config.APP_VERSION,"environment":Config.APP_ENV,"uptime_seconds":int(time.time()-START_TIME)})

@system_bp.get("/health")
def health():
 try:
  db.session.execute(db.text("SELECT 1")); database="online"
 except Exception: database="offline"
 return jsonify(success=database=="online",application=Config.APP_NAME,database=database)

@system_bp.get("/cache")
@require_admin
def cache_status():return jsonify(success=True,cache={"enabled":False,"status":"not_configured"})

@system_bp.post("/cache/clear")
@require_admin
def clear_cache():return jsonify(success=True,message="Aucun cache applicatif configuré")

@system_bp.post("/database/optimize")
@require_admin
def optimize_database():return jsonify(success=True,message="Optimisation PostgreSQL à effectuer selon l'hébergeur")

@system_bp.post("/backup")
@require_admin
def create_backup():return jsonify(success=False,message="Utiliser les sauvegardes PostgreSQL de l'hébergeur pour une sauvegarde fiable"),501

@system_bp.post("/backup/restore")
@require_admin
def restore_backup():return jsonify(success=False,message="Restauration via l'hébergeur PostgreSQL"),501

@system_bp.post("/restart")
@require_admin
def restart_services():return jsonify(success=False,message="Le redémarrage est géré par le processus d'hébergement"),501

@system_bp.get("/status")
def status():return jsonify(service="System",status="online")
