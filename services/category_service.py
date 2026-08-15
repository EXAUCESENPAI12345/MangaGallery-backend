"""
==================================
MANGA GALLERY
CATEGORY SERVICE
==================================
"""

from database import db

from models.category import Category


class CategoryService:


    # ==================================
    # GET ALL CATEGORIES
    # ==================================

    @staticmethod

    def get_all():

        return Category.query.all()


    # ==================================
    # GET ONE CATEGORY
    # ==================================

    @staticmethod

    def get_by_id(

        category_id

    ):

        return Category.query.get(

            category_id

        )


    # ==================================
    # SEARCH CATEGORY
    # ==================================

    @staticmethod

    def search(

        keyword

    ):

        return Category.query.filter(

            Category.name.ilike(

                f"%{keyword}%"

            )

        ).all()
        
        """
==================================
CREATE CATEGORY
==================================
"""

    @staticmethod

    def create(

        data

    ):

        category = Category(

            **data

        )

        db.session.add(

            category

        )

        db.session.commit()

        return category


    # ==================================
    # UPDATE CATEGORY
    # ==================================

    @staticmethod

    def update(

        category,

        data

    ):

        for key, value in data.items():

            setattr(

                category,

                key,

                value

            )

        db.session.commit()

        return category


    # ==================================
    # DELETE CATEGORY
    # ==================================

    @staticmethod

    def delete(

        category

    ):

        db.session.delete(

            category

        )

        db.session.commit()

        return True
        
        """
==================================
COUNT MANGAS
==================================
"""

    @staticmethod

    def manga_count(

        category

    ):

        return len(

            category.mangas

        )


    # ==================================
    # CATEGORY STATISTICS
    # ==================================

    @staticmethod

    def statistics():

        total_categories = Category.query.count()

        active_categories = Category.query.filter_by(

            is_active=True

        ).count()

        return {

            "total_categories": total_categories,

            "active_categories": active_categories

        }


    # ==================================
    # ACTIVATE CATEGORY
    # ==================================

    @staticmethod

    def set_status(

        category,

        is_active

    ):

        category.is_active = is_active

        db.session.commit()

        return category
