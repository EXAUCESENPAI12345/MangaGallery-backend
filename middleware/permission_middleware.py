"""
==================================
MANGA GALLERY
PERMISSION MIDDLEWARE
==================================
"""

from functools import wraps

from flask import jsonify

from middleware.auth_middleware import current_user


"""
==================================
REQUIRE PERMISSION
==================================
"""

def require_permission(

    permission

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

            permissions = user.role.permissions or {}

            if not permissions.get(

                permission,

                False

            ):

                return jsonify({

                    "success": False,

                    "message": "Permission refusée"

                }),403

            return function(

                *args,

                **kwargs

            )

        return wrapper

    return decorator


"""
==================================
GET PERMISSIONS
==================================
"""

def current_permissions():

    user = current_user()

    if not user:

        return {}

    return user.role.permissions
    
    """
==================================
CHECK PERMISSION
==================================
"""

def has_permission(

    permission

):

    permissions = current_permissions()

    return permissions.get(

        permission,

        False

    )


"""
==================================
MANAGE MANGAS
==================================
"""

def manage_mangas():

    return require_permission(

        "manage_mangas"

    )


"""
==================================
MANAGE USERS
==================================
"""

def manage_users():

    return require_permission(

        "manage_users"

    )
    
    """
==================================
CHECK PERMISSION
==================================
"""

def has_permission(

    permission

):

    permissions = current_permissions()

    return permissions.get(

        permission,

        False

    )


"""
==================================
MANAGE MANGAS
==================================
"""

def manage_mangas():

    return require_permission(

        "manage_mangas"

    )


"""
==================================
MANAGE USERS
==================================
"""

def manage_users():

    return require_permission(

        "manage_users"

    )
    
    """
==================================
MANAGE SETTINGS
==================================
"""

def manage_settings():

    return require_permission(

        "manage_settings"

    )


"""
==================================
MANAGE ROLES
==================================
"""

def manage_roles():

    return require_permission(

        "manage_roles"

    )


"""
==================================
MODERATE COMMENTS
==================================
"""

def moderate_comments():

    return require_permission(

        "moderate_comments"

    )


"""
==================================
PERMISSION DENIED
==================================
"""

def permission_denied():

    return jsonify({

        "success": False,

        "message": "Permissions insuffisantes"

    }),403