from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config, validate_config
from database import init_database, db

# Import all models before mapper configuration / create_all.
from models.user import User
from models.role import Role
from models.category import Category
from models.manga import Manga
from models.chapter import Chapter
from models.media import Media
from models.comment import Comment
from models.notification import Notification
from models.report import Report
from models.settings import Settings
from models.admin import Admin

validate_config()
app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}}, supports_credentials=True)
JWTManager(app)
init_database(app)

from routes.auth import auth_bp
from routes.mangas import mangas_bp
from routes.chapters import chapters_bp
from routes.categories import categories_bp
from routes.users import users_bp
from routes.comments import comments_bp
from routes.notifications import notifications_bp
from routes.statistics import statistics_bp
from routes.reports import reports_bp
from routes.media import media_bp
from routes.roles import roles_bp
from routes.settings import settings_bp
from routes.system import system_bp
from routes.telegram import telegram_bp

for blueprint, prefix in [
    (auth_bp, "/api/auth"), (mangas_bp, "/api/mangas"), (chapters_bp, "/api/chapters"),
    (categories_bp, "/api/categories"), (users_bp, "/api/users"), (comments_bp, "/api/comments"),
    (notifications_bp, "/api/notifications"), (statistics_bp, "/api/statistics"),
    (reports_bp, "/api/reports"), (media_bp, "/api/media"), (roles_bp, "/api/roles"),
    (settings_bp, "/api/settings"), (system_bp, "/api/system"), (telegram_bp, "/api/telegram")]:
    app.register_blueprint(blueprint, url_prefix=prefix)

@app.get("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        database = "online"
        status = "online"
    except Exception:
        database = "offline"
        status = "degraded"
    return {"status": status, "application": Config.APP_NAME, "version": Config.APP_VERSION, "database": database}, 200 if database == "online" else 503

@app.errorhandler(404)
def not_found(error): return {"success": False, "message": "Resource not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return {"success": False, "message": "Internal server error"}, 500

@app.errorhandler(Exception)
def global_exception(error):
    db.session.rollback()
    app.logger.exception("Unhandled application error")
    return {"success": False, "message": "Internal server error"}, 500

@app.after_request
def after_request(response):
    response.headers["X-App-Name"] = Config.APP_NAME
    response.headers["X-App-Version"] = Config.APP_VERSION
    return response

@app.cli.command("init-db")
def init_db_command():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

if __name__ == "__main__":
    if Config.AUTO_CREATE_TABLES:
        with app.app_context(): db.create_all()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
