"""
==================================
MANGA GALLERY
SETTINGS SERVICE
==================================
"""

from database import db

from models.settings import Settings


class SettingsService:


    """
    ==============================
    GET SETTINGS
    ==============================
    """

    @staticmethod

    def get():

        return Settings.query.first()


    """
    ==============================
    GET APPLICATION
    ==============================
    """

    @staticmethod

    def get_application():

        settings = Settings.query.first()

        return settings


    """
    ==============================
    GET TELEGRAM CONFIG
    ==============================
    """

    @staticmethod

    def get_telegram():

        settings = Settings.query.first()

        return {

            "telegram_bot": settings.telegram_bot,

            "mini_app_url": settings.mini_app_url,

            "backend_url": settings.backend_url

        }
        
        """
==================================
UPDATE SETTINGS
==================================
"""

    @staticmethod

    def update(

        data

    ):

        settings = Settings.query.first()

        for key, value in data.items():

            setattr(

                settings,

                key,

                value

            )

        db.session.commit()

        return settings


    # ==================================
    # UPDATE TELEGRAM
    # ==================================

    @staticmethod

    def update_telegram(

        telegram_bot,

        mini_app_url,

        backend_url

    ):

        settings = Settings.query.first()

        settings.telegram_bot = telegram_bot

        settings.mini_app_url = mini_app_url

        settings.backend_url = backend_url

        db.session.commit()

        return settings


    # ==================================
    # UPDATE URLS
    # ==================================

    @staticmethod

    def update_urls(

        mini_app_url,

        backend_url

    ):

        settings = Settings.query.first()

        settings.mini_app_url = mini_app_url

        settings.backend_url = backend_url

        db.session.commit()

        return settings
        
        """
==================================
MAINTENANCE MODE
==================================
"""

    @staticmethod

    def set_maintenance(

        enabled

    ):

        settings = Settings.query.first()

        settings.maintenance_mode = enabled

        db.session.commit()

        return settings


    # ==================================
    # UPDATE LANGUAGE
    # ==================================

    @staticmethod

    def update_language(

        language

    ):

        settings = Settings.query.first()

        settings.default_language = language

        db.session.commit()

        return settings


    # ==================================
    # SETTINGS STATISTICS
    # ==================================

    @staticmethod

    def statistics():

        settings = Settings.query.first()

        return {

            "app_name": settings.app_name,

            "maintenance_mode": settings.maintenance_mode,

            "registration_enabled": settings.registration_enabled,

            "default_language": settings.default_language

        }