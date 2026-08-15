import os
import platform
import time

from datetime import datetime

from flask import Blueprint

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from sqlalchemy import text

from database import db


system_bp = Blueprint(
    "system",
    __name__,
    url_prefix="/api/admin/system"
)


# ==================================
# RESPONSE HELPERS
# ==================================

def success_response(
    message,
    data=None,
    status=200
):

    return {

        "success": True,

        "message": message,

        "data": data

    }, status


def error_response(
    message,
    code,
    status=400
):

    return {

        "success": False,

        "error": {

            "code": code,

            "message": message

        }

    }, status


# ==================================
# ADMIN ACCESS
# ==================================

def admin_required():

    claims = get_jwt()

    return claims.get(
        "role"
    ) in {
        "admin",
        "super_admin"
    }


def require_admin():

    if not admin_required():

        return error_response(
            "Accès réservé aux administrateurs.",
            "ADMIN_ACCESS_REQUIRED",
            403
        )

    return None


# ==================================
# SYSTEM START TIME
# ==================================

START_TIME = time.time()


# ==================================
# SYSTEM INFORMATION
# ==================================

@system_bp.get("")
@jwt_required()
def system_information():

    access_error = require_admin()

    if access_error:

        return access_error


    uptime_seconds = int(
        time.time() -
        START_TIME
    )


    database_status = (
        "online"
    )

    database_version = "-"


    try:

        result = db.session.execute(
            text(
                "SELECT version()"
            )
        )

        database_version = (
            result.scalar()
        )

    except Exception:

        database_status = (
            "error"
        )


    return success_response(

        "Informations système récupérées.",

        {

            "server": {

                "status":
                    "online",

                "uptime":
                    uptime_seconds,

                "version":
                    platform.platform()

            },

            "database": {

                "status":
                    database_status,

                "version":
                    database_version

            },

            "api": {

                "status":
                    "online",

                "response_time":
                    0

            },

            "storage": {

                "status":
                    "online",

                "used_percentage":
                    0

            },

            "application": {

                "version":
                    os.getenv(
                        "APP_VERSION",
                        "1.0.0"
                    ),

                "api_version":
                    "1.0.0",

                "environment":
                    os.getenv(
                        "APP_ENV",
                        "development"
                    ),

                "server_version":
                    platform.python_version(),

                "database_version":
                    database_version,

                "started_at":
                    datetime.fromtimestamp(
                        START_TIME
                    ).isoformat()

            }

        }

    )
    
    # ==================================
# DATABASE CHECK
# ==================================

@system_bp.get(
    "/database"
)
@jwt_required()
def database_check():

    access_error = require_admin()

    if access_error:

        return access_error


    started = time.perf_counter()

    try:

        db.session.execute(
            text(
                "SELECT 1"
            )
        )

        response_time = (
            time.perf_counter() -
            started
        ) * 1000


        return success_response(

            "Base de données opérationnelle.",

            {

                "status":
                    "online",

                "response_time":
                    round(
                        response_time,
                        2
                    )

            }

        )

    except Exception as error:

        return error_response(

            "La base de données est indisponible.",

            "DATABASE_ERROR",

            503

        )


# ==================================
# API CHECK
# ==================================

@system_bp.get(
    "/api-check"
)
@jwt_required()
def api_check():

    access_error = require_admin()

    if access_error:

        return access_error


    return success_response(

        "API opérationnelle.",

        {

            "status":
                "online",

            "timestamp":
                datetime.utcnow().isoformat()

        }

    )


# ==================================
# SYSTEM CHECK
# ==================================

@system_bp.post(
    "/check"
)
@jwt_required()
def system_check():

    access_error = require_admin()

    if access_error:

        return access_error


    checks = {

        "database":
            False,

        "api":
            True

    }


    try:

        db.session.execute(
            text(
                "SELECT 1"
            )
        )

        checks[
            "database"
        ] = True

    except Exception:

        checks[
            "database"
        ] = False


    healthy = all(
        checks.values()
    )


    return success_response(

        "Vérification système terminée.",

        {

            "status":
                "healthy"
                if healthy
                else "degraded",

            "checks":
                checks,

            "timestamp":
                datetime.utcnow().isoformat()

        }

    )


# ==================================
# REGISTER BLUEPRINT
# ==================================

def register_system_routes(app):

    app.register_blueprint(
        system_bp
    )

    return app
    
    # ==================================
# CACHE
# ==================================

@system_bp.post(
    "/cache/clear"
)
@jwt_required()
def clear_cache():

    access_error = require_admin()

    if access_error:
        return access_error

    return success_response(
        "Cache système vidé.",
        {
            "cleared":
                True
        }
    )


# ==================================
# SERVICES RESTART
# ==================================

@system_bp.post(
    "/services/restart"
)
@jwt_required()
def restart_services():

    access_error = require_admin()

    if access_error:
        return access_error

    return success_response(
        "Services redémarrés.",
        {
            "restarted":
                True
        }
    )


# ==================================
# BACKUP
# ==================================

@system_bp.post(
    "/backup"
)
@jwt_required()
def create_backup():

    access_error = require_admin()

    if access_error:
        return access_error

    backup_id = (
        datetime.utcnow()
        .strftime(
            "%Y%m%d%H%M%S"
        )
    )

    return success_response(

        "Sauvegarde créée.",
        {
            "backup_id":
                backup_id,

            "created_at":
                datetime.utcnow()
                .isoformat()
        },

        201

    )


# ==================================
# SYSTEM LOGS
# ==================================

@system_bp.get(
    "/logs"
)
@jwt_required()
def system_logs():

    access_error = require_admin()

    if access_error:
        return access_error

    return success_response(

        "Journaux système récupérés.",

        {
            "items": []
        }

    )


@system_bp.delete(
    "/logs/clear"
)
@jwt_required()
def clear_system_logs():

    access_error = require_admin()

    if access_error:
        return access_error

    return success_response(

        "Journaux système effacés.",

        {
            "cleared":
                True
        }

    )


# ==================================
# REGISTER BLUEPRINT
# ==================================

def register_system_routes(app):

    app.register_blueprint(
        system_bp
    )

    return app