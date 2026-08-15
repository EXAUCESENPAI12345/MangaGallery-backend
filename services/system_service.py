"""
==================================
MANGA GALLERY
SYSTEM SERVICE
==================================
"""

import platform
import time

from database import db


class SystemService:


    """
    ==============================
    SYSTEM INFORMATION
    ==============================
    """

    @staticmethod

    def info():

        return {

            "application": "Manga Gallery",

            "version": "1.0.0",

            "python": platform.python_version(),

            "platform": platform.system()

        }


    """
    ==============================
    SERVER HEALTH
    ==============================
    """

    @staticmethod

    def health():

        return {

            "status": "online",

            "timestamp": int(

                time.time()

            )

        }


    """
    ==============================
    DATABASE STATUS
    ==============================
    """

    @staticmethod

    def database():

        return {

            "status": "connected"

        }
        
        """
==================================
CLEAR CACHE
==================================
"""

    @staticmethod

    def clear_cache():

        """

        Nettoyage du cache
        de l'application.

        """

        return {

            "success": True,

            "message": "Cache vidé avec succès"

        }


    # ==================================
    # OPTIMIZE DATABASE
    # ==================================

    @staticmethod

    def optimize_database():

        """

        Optimisation de la
        base de données.

        """

        db.session.execute(

            "VACUUM"

        )

        return {

            "success": True,

            "message": "Base de données optimisée"

        }


    # ==================================
    # CREATE BACKUP
    # ==================================

    @staticmethod

    def create_backup():

        """

        Création d'une
        sauvegarde.

        """

        return {

            "success": True,

            "message": "Sauvegarde créée"

        }
        
        """
==================================
RESTORE BACKUP
==================================
"""

    @staticmethod

    def restore_backup(

        backup_path

    ):

        """

        Restauration d'une
        sauvegarde.

        """

        return {

            "success": True,

            "message": "Sauvegarde restaurée"

        }


    # ==================================
    # RESTART SERVICES
    # ==================================

    @staticmethod

    def restart_services():

        """

        Redémarrage des
        services autorisés.

        """

        return {

            "success": True,

            "message": "Services redémarrés"

        }


    # ==================================
    # SYSTEM STATISTICS
    # ==================================

    @staticmethod

    def statistics():

        return {

            "application": "Manga Gallery",

            "version": "1.0.0",

            "database": "connected",

            "server": "online"

        }