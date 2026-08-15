"""
==================================
MANGA GALLERY
ROLE MIDDLEWARE
==================================
"""

from functools import wraps

from flask import jsonify

from middleware.auth_middleware import current_user


"""
==================================
REQUIRE ROLE
==================================
"""

def require_role(

    *roles

):

    def decorator(

        function

    ):

        @wraps(function)

        def wrapper(

            *args,

            **kwargs

        ):

            user = current_user()

            if not user:

                return jsonify({

                    "success": False,

                    "message": "Utilisateur introuvable"

                }),404

            if user.role.name not in roles:

                return jsonify({

                    "success": False,

                    "message": "Accès refusé"

                }),403

            return function(

                *args,

                **kwargs

            )

        return wrapper

    return decorator


"""
==================================
GET CURRENT ROLE
==================================
"""

def current_role():

    user = current_user()

    if not user:

        return None

    return user.role
    
    """
==================================
SUPER ADMIN
==================================
"""

def require_super_admin():

    return require_role(

        "super_admin"

    )


"""
==================================
ADMIN
==================================
"""

def require_admin():

    return require_role(

        "super_admin",

        "admin"

    )


"""
==================================
MODERATOR
==================================
"""

def require_moderator():

    return require_role(

        "super_admin",

        "admin",

        "moderator"

    )
    
    """
==================================
MULTIPLE ROLES
==================================
"""

def has_any_role(

    *roles

):

    user = current_user()

    if not user:

        return False

    return user.role.name in roles


"""
==================================
ACCESS DENIED
==================================
"""

def access_denied():

    return jsonify({

        "success": False,

        "message": "Vous n'avez pas les permissions nécessaires"

    }),403


"""
==================================
CHECK ROLE
==================================
"""

def check_role(

    role_name

):

    user = current_user()

    if not user:

        return False

    return user.role.name == role_name