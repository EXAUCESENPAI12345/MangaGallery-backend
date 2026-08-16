import os

from pathlib import Path

from dotenv import load_dotenv


# ==================================
# ENVIRONNEMENT
# ==================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    BASE_DIR / ".env"
)


# ==================================
# CONFIGURATION
# ==================================

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )

    JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "change-this-jwt-secret-key"
)
        
# PostgreSQL
# ------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    ""
)

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

SQLALCHEMY_DATABASE_URI = DATABASE_URL

SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ------------------------------
    # Application
    # ------------------------------

    APP_NAME = os.getenv(
        "APP_NAME",
        "Manga Gallery"
    )

    APP_ENV = os.getenv(
        "APP_ENV",
        "development"
    )

    DEBUG = (
        APP_ENV == "development"
    )

    HOST = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )


    AUTO_CREATE_TABLES = os.getenv("AUTO_CREATE_TABLES", "false").lower() in {"1", "true", "yes"}

    # ------------------------------
    # API
    # ------------------------------

    API_PREFIX = os.getenv(
        "API_PREFIX",
        "/api"
    )


    # ------------------------------
    # Upload / médias
    # ------------------------------

    MAX_CONTENT_LENGTH = (
        50 * 1024 * 1024
    )

    ALLOWED_IMAGE_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "webp"
    }


    # ------------------------------
    # Pagination
    # ------------------------------

    DEFAULT_PAGE_SIZE = int(
        os.getenv(
            "DEFAULT_PAGE_SIZE",
            "20"
        )
    )

    MAX_PAGE_SIZE = int(
        os.getenv(
            "MAX_PAGE_SIZE",
            "100"
        )
    )


    # ------------------------------
    # CORS
    # ------------------------------

    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "*"
    )


    # ------------------------------
    # Telegram
    # ------------------------------

    TELEGRAM_BOT_TOKEN = os.getenv(
        "TELEGRAM_BOT_TOKEN",
        ""
    )

    TELEGRAM_BOT_USERNAME = os.getenv(
        "TELEGRAM_BOT_USERNAME",
        ""
    )

    TELEGRAM_MINI_APP_URL = os.getenv(
        "TELEGRAM_MINI_APP_URL",
        ""
    )

    TELEGRAM_WEBHOOK_SECRET = os.getenv(
        "TELEGRAM_WEBHOOK_SECRET",
        ""
    )

    PUBLIC_BACKEND_URL = os.getenv(
        "PUBLIC_BACKEND_URL",
        ""
    )


# ==================================
# VALIDATION
# ==================================

def validate_config():

    required = {

        "SECRET_KEY":
            Config.SECRET_KEY,

        "JWT_SECRET_KEY":
            Config.JWT_SECRET_KEY,

        "DATABASE_URL":
            Config.DATABASE_URL

    }

    missing = [

        key

        for key, value
        in required.items()

        if not value

    ]


    if missing:

        raise RuntimeError(
            "Configuration manquante : "
            + ", ".join(missing)
        )


    return True
