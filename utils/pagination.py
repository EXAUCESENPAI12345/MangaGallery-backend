"""
==================================
MANGA GALLERY
PAGINATION UTILS
==================================
"""


"""
==================================
PAGINATE QUERY
==================================
"""

def paginate(

    query,

    page=1,

    per_page=20

):

    return query.paginate(

        page=page,

        per_page=per_page,

        error_out=False

    )


"""
==================================
CURRENT PAGE
==================================
"""

def current_page(

    pagination

):

    return pagination.page


"""
==================================
TOTAL PAGES
==================================
"""

def total_pages(

    pagination

):

    return pagination.pages
    
    """
==================================
TOTAL ITEMS
==================================
"""

def total_items(

    pagination

):

    return pagination.total


"""
==================================
PREVIOUS PAGE
==================================
"""

def previous_page(

    pagination

):

    return pagination.prev_num if pagination.has_prev else None


"""
==================================
NEXT PAGE
==================================
"""

def next_page(

    pagination

):

    return pagination.next_num if pagination.has_next else None
    
    """
==================================
PAGINATION RESPONSE
==================================
"""

def pagination_response(

    pagination

):

    return {

        "page": pagination.page,

        "per_page": pagination.per_page,

        "total_items": pagination.total,

        "total_pages": pagination.pages,

        "previous_page": previous_page(

            pagination

        ),

        "next_page": next_page(

            pagination

        )

    }


"""
==================================
PAGINATED DATA
==================================
"""

def paginated_data(

    pagination

):

    return {

        "items": [

            item.to_dict()

            for item in pagination.items

        ],

        "pagination": pagination_response(

            pagination

        )

    }


"""
==================================
HAS NEXT / PREVIOUS
==================================
"""

def navigation(

    pagination

):

    return {

        "has_next": pagination.has_next,

        "has_previous": pagination.has_prev

    }