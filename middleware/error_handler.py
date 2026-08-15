"""
==================================
MANGA GALLERY
ERROR HANDLER
==================================
"""

from flask import jsonify


"""
==================================
BAD REQUEST
==================================
"""

def bad_request(

    message="Requête invalide"

):

    return jsonify({

        "success": False,

        "error": message

    }),400


"""
==================================
UNAUTHORIZED
==================================
"""

def unauthorized(

    message="Non autorisé"

):

    return jsonify({

        "success": False,

        "error": message

    }),401


"""
==================================
FORBIDDEN
==================================
"""

def forbidden(

    message="Accès interdit"

):

    return jsonify({

        "success": False,

        "error": message

    }),403
    
    """
==================================
NOT FOUND
==================================
"""

def not_found(

    message="Ressource introuvable"

):

    return jsonify({

        "success": False,

        "error": message

    }),404


"""
==================================
INTERNAL SERVER ERROR
==================================
"""

def internal_server_error(

    message="Erreur interne du serveur"

):

    return jsonify({

        "success": False,

        "error": message

    }),500


"""
==================================
LOG ERROR
==================================
"""

def log_error(

    error

):

    print(

        f"[ERROR] {error}"

    )
    
    """
==================================
JSON ERROR RESPONSE
==================================
"""

def error_response(

    status_code,

    message

):

    return jsonify({

        "success": False,

        "status": status_code,

        "error": message

    }), status_code


"""
==================================
GLOBAL EXCEPTION HANDLER
==================================
"""

def register_error_handlers(

    app

):

    @app.errorhandler(Exception)

    def handle_exception(

        error

    ):

        log_error(

            error

        )

        return internal_server_error(

            str(error)

        )


"""
==================================
SUCCESS RESPONSE
==================================
"""

def success_response(

    message,

    data=None

):

    return jsonify({

        "success": True,

        "message": message,

        "data": data

    }),200