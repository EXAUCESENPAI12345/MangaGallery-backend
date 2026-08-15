"""
==================================
MANGA GALLERY
JWT UTILS
==================================
"""

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import decode_token


"""
==================================
CREATE ACCESS TOKEN
==================================
"""

def generate_access_token(

    user_id

):

    return create_access_token(

        identity=user_id

    )


"""
==================================
CREATE REFRESH TOKEN
==================================
"""

def generate_refresh_token(

    user_id

):

    return create_refresh_token(

        identity=user_id

    )


"""
==================================
CREATE TOKEN PAIR
==================================
"""

def generate_tokens(

    user_id

):

    return {

        "access_token": generate_access_token(

            user_id

        ),

        "refresh_token": generate_refresh_token(

            user_id

        )

    }
    
    """
==================================
DECODE TOKEN
==================================
"""

def decode_jwt(

    token

):

    return decode_token(

        token

    )


"""
==================================
VERIFY TOKEN
==================================
"""

def verify_token(

    token

):

    try:

        decode_token(

            token

        )

        return True

    except Exception:

        return False


"""
==================================
TOKEN EXPIRED
==================================
"""

def is_token_expired(

    token

):

    try:

        payload = decode_token(

            token

        )

        return payload.get(

            "exp",

            0

        ) <= payload.get(

            "iat",

            0

        )

    except Exception:

        return True
        
        """
==================================
REFRESH ACCESS TOKEN
==================================
"""

def refresh_access_token(

    user_id

):

    return generate_access_token(

        user_id

    )


"""
==================================
REVOKE TOKEN
==================================
"""

def revoke_token(

    token

):

    """

    Si une blacklist JWT
    est utilisée, le token
    sera enregistré ici.

    """

    return True


"""
==================================
GET USER ID
==================================
"""

def get_user_id(

    token

):

    payload = decode_token(

        token

    )

    return payload.get(

        "sub"

    )