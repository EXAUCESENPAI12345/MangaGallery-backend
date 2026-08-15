from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# ==================================
# EXTENSIONS
# ==================================

db = SQLAlchemy()
migrate = Migrate()


# ==================================
# INITIALISATION
# ==================================

def init_database(app):
    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    return db


# ==================================
# CREATE TABLES
# ==================================

def create_database():
    with db.engine.begin() as connection:
        db.metadata.create_all(connection)


# ==================================
# DROP TABLES
# ==================================

def drop_database():
    with db.engine.begin() as connection:
        db.metadata.drop_all(connection)


# ==================================
# RESET DATABASE
# ==================================

def reset_database():
    drop_database()
    create_database()


# ==================================
# CLOSE SESSION
# ==================================

def close_session(exception=None):
    """Nettoie la session SQLAlchemy après chaque requête."""
    db.session.remove()
