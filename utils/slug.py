"""
==================================
MANGA GALLERY
SLUG UTILS
==================================
"""

import re

import unicodedata


"""
==================================
SLUGIFY
==================================
"""

def slugify(

    text

):

    text = unicodedata.normalize(

        "NFKD",

        text

    ).encode(

        "ascii",

        "ignore"

    ).decode(

        "ascii"

    )

    text = text.lower()

    text = re.sub(

        r"[^a-z0-9]+",

        "-",

        text

    )

    return text.strip(

        "-"

    )


"""
==================================
MANGA SLUG
==================================
"""

def manga_slug(

    title

):

    return slugify(

        title

    )


"""
==================================
CATEGORY SLUG
==================================
"""

def category_slug(

    name

):

    return slugify(

        name

    )
    
    """
==================================
CHAPTER SLUG
==================================
"""

def chapter_slug(

    title

):

    return slugify(

        title

    )


"""
==================================
UPDATE SLUG
==================================
"""

def update_slug(

    old_slug,

    new_value

):

    """

    Génère un nouveau slug
    à partir de la nouvelle valeur.

    """

    return slugify(

        new_value

    )


"""
==================================
VALIDATE SLUG
==================================
"""

def validate_slug(

    slug

):

    pattern = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"

    return bool(

        re.match(

            pattern,

            slug

        )

    )
    
    """
==================================
UNIQUE SLUG
==================================
"""

def unique_slug(

    slug,

    exists_callback

):

    new_slug = slug

    counter = 1

    while exists_callback(

        new_slug

    ):

        new_slug = f"{slug}-{counter}"

        counter += 1

    return new_slug


"""
==================================
SLUG LENGTH
==================================
"""

def validate_slug_length(

    slug,

    minimum=3,

    maximum=120

):

    return minimum <= len(

        slug

    ) <= maximum


"""
==================================
SLUG INFORMATION
==================================
"""

def slug_info(

    slug

):

    return {

        "slug": slug,

        "length": len(slug),

        "valid": validate_slug(slug),

        "seo_friendly": "-" in slug

    }