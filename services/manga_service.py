"""
==================================
MANGA GALLERY
MANGA SERVICE
==================================
"""

from database import db

from models.manga import Manga


class MangaService:


    """
    ==============================
    GET ALL MANGAS
    ==============================
    """

    @staticmethod

    def get_all():

        return Manga.query.all()


    """
    ==============================
    GET ONE MANGA
    ==============================
    """

    @staticmethod

    def get_by_id(

        manga_id

    ):

        return Manga.query.get(

            manga_id

        )


    """
    ==============================
    SEARCH
    ==============================
    """

    @staticmethod

    def search(

        keyword

    ):

        return Manga.query.filter(

            Manga.title.ilike(

                f"%{keyword}%"

            )

        ).all()
        
        """
==================================
CREATE MANGA
==================================
"""

    @staticmethod

    def create(

        data

    ):

        manga = Manga(

            **data

        )

        db.session.add(

            manga

        )

        db.session.commit()

        return manga


    # ==================================
    # UPDATE MANGA
    # ==================================

    @staticmethod

    def update(

        manga,

        data

    ):

        for key, value in data.items():

            setattr(

                manga,

                key,

                value

            )

        db.session.commit()

        return manga


    # ==================================
    # DELETE MANGA
    # ==================================

    @staticmethod

    def delete(

        manga

    ):

        db.session.delete(

            manga

        )

        db.session.commit()

        return True
        
        """
==================================
UPDATE VIEWS
==================================
"""

    @staticmethod

    def increment_views(

        manga

    ):

        manga.views += 1

        db.session.commit()

        return manga


    # ==================================
    # UPDATE FAVORITES
    # ==================================

    @staticmethod

    def update_favorites(

        manga,

        increment=True

    ):

        if increment:

            manga.favorites += 1

        elif manga.favorites > 0:

            manga.favorites -= 1

        db.session.commit()

        return manga


    # ==================================
    # UPDATE RATING
    # ==================================

    @staticmethod

    def update_rating(

        manga,

        rating

    ):

        manga.rating = rating

        db.session.commit()

        return manga