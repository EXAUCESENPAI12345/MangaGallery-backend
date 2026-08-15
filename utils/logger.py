"""
==================================
MANGA GALLERY
LOGGER UTILS
==================================
"""

import logging

import os


"""
==================================
CREATE LOGGER
==================================
"""

def create_logger(

    name,

    log_file

):

    logger = logging.getLogger(

        name

    )

    logger.setLevel(

        logging.INFO

    )

    os.makedirs(

        os.path.dirname(

            log_file

        ),

        exist_ok=True

    )

    handler = logging.FileHandler(

        log_file,

        encoding="utf-8"

    )

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s"

    )

    handler.setFormatter(

        formatter

    )

    logger.addHandler(

        handler

    )

    return logger


"""
==================================
APPLICATION LOGGER
==================================
"""

app_logger = create_logger(

    "application",

    "logs/application.log"

)


"""
==================================
ERROR LOGGER
==================================
"""

error_logger = create_logger(

    "errors",

    "logs/error.log"

)

"""
==================================
LOG ERROR
==================================
"""

def log_error(

    message

):

    error_logger.error(

        message

    )


"""
==================================
LOG LOGIN
==================================
"""

def log_login(

    username

):

    app_logger.info(

        f"Connexion : {username}"

    )


"""
==================================
LOG USER ACTION
==================================
"""

def log_user_action(

    username,

    action

):

    app_logger.info(

        f"Utilisateur {username} : {action}"

    )
    
    """
==================================
LOG ADMIN ACTION
==================================
"""

def log_admin_action(

    username,

    action

):

    app_logger.info(

        f"Administrateur {username} : {action}"

    )


"""
==================================
LOG SYSTEM EVENT
==================================
"""

def log_system_event(

    event

):

    app_logger.info(

        f"Système : {event}"

    )


"""
==================================
LOG FILE UPLOAD
==================================
"""

def log_upload(

    filename,

    username

):

    app_logger.info(

        f"Upload : {filename} par {username}"

    )