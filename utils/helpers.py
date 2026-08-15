"""
==================================
MANGA GALLERY
HELPERS
==================================
"""

import uuid

from datetime import datetime


"""
==================================
GENERATE UUID
==================================
"""

def generate_uuid():

    return str(

        uuid.uuid4()

    )


"""
==================================
CURRENT DATETIME
==================================
"""

def now():

    return datetime.utcnow()


"""
==================================
CURRENT TIMESTAMP
==================================
"""

def timestamp():

    return int(

        datetime.utcnow().timestamp()

    )
    
    """
==================================
FORMAT FILE SIZE
==================================
"""

def format_file_size(

    size

):

    for unit in [

        "B",

        "KB",

        "MB",

        "GB",

        "TB"

    ]:

        if size < 1024:

            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


"""
==================================
FORMAT NUMBER
==================================
"""

def format_number(

    value

):

    return f"{value:,}"


"""
==================================
CLEAN STRING
==================================
"""

def clean_string(

    value

):

    return value.strip()
    
    """
==================================
GENERATE RANDOM CODE
==================================
"""

import random

import string


def random_code(

    length=8

):

    characters = (

        string.ascii_uppercase

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
CHECK EMPTY VALUE
==================================
"""

def is_empty(

    value

):

    return value is None or str(

        value

    ).strip() == ""


"""
==================================
TO BOOLEAN
==================================
"""

def to_bool(

    value

):

    if isinstance(

        value,

        bool

    ):

        return value

    return str(

        value

    ).lower() in (

        "true",

        "1",

        "yes",

        "on"

    )