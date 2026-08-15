"""
==================================
MANGA GALLERY
PASSWORD UTILS
==================================
"""

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


"""
==================================
HASH PASSWORD
==================================
"""

def hash_password(

    password

):

    return generate_password_hash(

        password

    )


"""
==================================
VERIFY PASSWORD
==================================
"""

def verify_password(

    password,

    password_hash

):

    return check_password_hash(

        password_hash,

        password

    )
    
    """
==================================
PASSWORD STRENGTH
==================================
"""

import random
import string


def is_strong_password(

    password

):

    return (

        len(password) >= 8

        and any(

            c.isupper()

            for c in password

        )

        and any(

            c.islower()

            for c in password

        )

        and any(

            c.isdigit()

            for c in password

        )

    )


"""
==================================
TEMPORARY PASSWORD
==================================
"""

def temporary_password(

    length=10

):

    characters = (

        string.ascii_letters

        + string.digits

    )

    return "".join(

        random.choice(

            characters

        )

        for _ in range(

            length

        )

    )


"""
==================================
RANDOM PASSWORD
==================================
"""

def random_password(

    length=16

):

    characters = (

        string.ascii_letters

        + string.digits

        + "!@#$%^&*"

    )

    return "".join(

        random.choice(

            characters

        )

        for _ in range(

            length

        )

    )
    
    """
==================================
PASSWORD VALIDATION
==================================
"""

def validate_password(

    password

):

    if len(password) < 8:

        return False, "Le mot de passe doit contenir au moins 8 caractères."

    if len(password) > 128:

        return False, "Le mot de passe est trop long."

    if not any(c.isupper() for c in password):

        return False, "Le mot de passe doit contenir une lettre majuscule."

    if not any(c.islower() for c in password):

        return False, "Le mot de passe doit contenir une lettre minuscule."

    if not any(c.isdigit() for c in password):

        return False, "Le mot de passe doit contenir un chiffre."

    return True, "Mot de passe valide."


"""
==================================
PASSWORD SECURITY
==================================
"""

def password_security(

    password

):

    return {

        "length": len(password),

        "strong": is_strong_password(password),

        "valid": validate_password(password)[0]

    }


"""
==================================
PASSWORD LENGTH
==================================
"""

def password_length(

    password,

    minimum=8,

    maximum=128

):

    return minimum <= len(password) <= maximum