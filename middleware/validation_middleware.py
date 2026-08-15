"""
==================================
MANGA GALLERY
VALIDATION MIDDLEWARE
==================================
"""

import re

from flask import jsonify
from flask import request


"""
==================================
REQUIRED FIELDS
==================================
"""

def validate_required(

    *fields

):

    data = request.get_json()

    for field in fields:

        if field not in data:

            return jsonify({

                "success": False,

                "message": f"Le champ '{field}' est obligatoire"

            }),400

    return None


"""
==================================
EMAIL VALIDATION
==================================
"""

def validate_email(

    email

):

    pattern = r"^[^@]+@[^@]+\.[^@]+$"

    return bool(

        re.match(

            pattern,

            email

        )

    )


"""
==================================
USERNAME VALIDATION
==================================
"""

def validate_username(

    username

):

    return len(

        username

    ) >= 3
    
    """
==================================
PASSWORD VALIDATION
==================================
"""

def validate_password(

    password

):

    return len(

        password

    ) >= 8


"""
==================================
NUMBER VALIDATION
==================================
"""

def validate_number(

    value

):

    return isinstance(

        value,

        (

            int,

            float

        )

    )


"""
==================================
STRING LENGTH
==================================
"""

def validate_length(

    value,

    minimum,

    maximum

):

    return minimum <= len(

        value

    ) <= maximum
    
    """
==================================
FILE VALIDATION
==================================
"""

def validate_file(

    file,

    allowed_extensions

):

    if not file:

        return False

    filename = file.filename.lower()

    return filename.endswith(

        tuple(

            allowed_extensions

        )

    )


"""
==================================
VALIDATION ERROR
==================================
"""

def validation_error(

    message

):

    return jsonify({

        "success": False,

        "message": message

    }),400


"""
==================================
SUCCESS RESPONSE
==================================
"""

def validation_success():

    return jsonify({

        "success": True,

        "message": "Validation réussie"

    }),200