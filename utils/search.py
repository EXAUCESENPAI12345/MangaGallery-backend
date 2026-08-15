"""
==================================
MANGA GALLERY
SEARCH UTILS
==================================
"""

from sqlalchemy import or_


"""
==================================
SEARCH BY TITLE
==================================
"""

def search_title(

    model,

    keyword

):

    return model.query.filter(

        model.title.ilike(

            f"%{keyword}%"

        )

    )


"""
==================================
SEARCH BY NAME
==================================
"""

def search_name(

    model,

    keyword

):

    return model.query.filter(

        model.name.ilike(

            f"%{keyword}%"

        )

    )


"""
==================================
GLOBAL SEARCH
==================================
"""

def global_search(

    model,

    keyword,

    *fields

):

    filters = [

        getattr(

            model,

            field

        ).ilike(

            f"%{keyword}%"

        )

        for field in fields

    ]

    return model.query.filter(

        or_(

            *filters

        )

    )
    
    """
==================================
FILTER SEARCH
==================================
"""

def filter_search(

    query,

    **filters

):

    for field, value in filters.items():

        if value is not None:

            query = query.filter(

                getattr(

                    query.column_descriptions[0]["entity"],

                    field

                ) == value

            )

    return query


"""
==================================
ORDER RESULTS
==================================
"""

def order_results(

    query,

    field,

    descending=False

):

    column = getattr(

        query.column_descriptions[0]["entity"],

        field

    )

    if descending:

        return query.order_by(

            column.desc()

        )

    return query.order_by(

        column.asc()

    )


"""
==================================
PAGINATED SEARCH
==================================
"""

def paginated_search(

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
EXACT SEARCH
==================================
"""

def exact_search(

    model,

    field,

    value

):

    return model.query.filter(

        getattr(

            model,

            field

        ) == value

    )


"""
==================================
CASE INSENSITIVE SEARCH
==================================
"""

def insensitive_search(

    model,

    field,

    keyword

):

    return model.query.filter(

        getattr(

            model,

            field

        ).ilike(

            f"%{keyword}%"

        )

    )


"""
==================================
COUNT RESULTS
==================================
"""

def count_results(

    query

):

    return query.count()