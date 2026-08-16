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

    # ------------------------------
    # Security
    # ------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "change-this-jwt-secret-key"
    )


    # ------------------------------
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
            "10000"
        )
    )


    # ------------------------------
    # CORS
    # ------------------------------

    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "*"
    )

    if CORS_ORIGINS != "*":
        CORS_ORIGINS = [
            origin.strip()
            for origin in CORS_ORIGINS.split(",")
            if origin.strip()
        ]


    # ------------------------------
    # Database
    # ------------------------------

    AUTO_CREATE_TABLES = (
        os.getenv(
            "AUTO_CREATE_TABLES",
            "false"
        ).lower()
        == "true"
    )


    # ------------------------------
    # Telegram
    # ------------------------------

    TELEGRAM_BOT_TOKEN = os.getenv(
        "TELEGRAM_BOT_TOKEN",
        ""
    )

    TELEGRAM_WEBHOOK_SECRET = os.getenv(
        "TELEGRAM_WEBHOOK_SECRET",
        ""
    )


    # ------------------------------
    # Public URL
    # ------------------------------

    PUBLIC_BACKEND_URL = os.getenv(
        "PUBLIC_BACKEND_URL",
        ""
    )


    # ------------------------------
    # Version
    # ------------------------------

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
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
        for key, value in required.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Configuration manquante : "
            + ", ".join(missing)
        )

    return True
