from flask import Blueprint, request, jsonify
from database import db
from models.settings import Settings
from config import Config
from utils.authz import require_admin

settings_bp=Blueprint("settings",__name__)

def get_or_create():
 s=Settings.query.first()
 if not s:
  s=Settings(app_name=Config.APP_NAME,default_language="fr",registration_enabled=True,maintenance_mode=False);db.session.add(s);db.session.commit()
 return s

@settings_bp.get("/")
@require_admin
def get_settings():return jsonify(success=True,settings=get_or_create().to_dict())

@settings_bp.get("/application")
def get_application():return jsonify(success=True,application={"name":Config.APP_NAME,"version":Config.APP_VERSION,"environment":Config.APP_ENV})

@settings_bp.get("/telegram")
@require_admin
def get_telegram():return jsonify(success=True,telegram={"bot_username":Config.TELEGRAM_BOT_USERNAME,"configured":bool(Config.TELEGRAM_BOT_TOKEN)})

@settings_bp.put("/")
@require_admin
def update_settings():
 s=get_or_create();data=request.get_json(silent=True) or {}
 for f in ("app_name","mini_app_url","backend_url","logo","favicon","default_language","maintenance_mode","registration_enabled"):
  if f in data:setattr(s,f,data[f])
 db.session.commit();return jsonify(success=True,message="Paramètres mis à jour",settings=s.to_dict())

@settings_bp.patch("/telegram")
@require_admin
def update_telegram():return jsonify(success=False,message="Le token Telegram doit être géré par la variable d'environnement TELEGRAM_BOT_TOKEN"),400

@settings_bp.patch("/urls")
@require_admin
def update_urls():
 s=get_or_create();data=request.get_json(silent=True) or {}
 for f in ("mini_app_url","backend_url"):
  if f in data:setattr(s,f,data[f])
 db.session.commit();return jsonify(success=True,message="URLs mises à jour",settings=s.to_dict())

@settings_bp.patch("/maintenance")
@require_admin
def maintenance_mode():
 s=get_or_create();s.maintenance_mode=bool((request.get_json(silent=True) or {}).get("maintenance_mode"));db.session.commit();return jsonify(success=True,maintenance_mode=s.maintenance_mode)

@settings_bp.patch("/language")
@require_admin
def update_language():
 s=get_or_create();lang=str((request.get_json(silent=True) or {}).get("language","fr")).strip();
 if not lang:return jsonify(success=False,message="Langue invalide"),400
 s.default_language=lang;db.session.commit();return jsonify(success=True,language=s.default_language)

@settings_bp.get("/status")
def status():return jsonify(service="Settings",status="online")
