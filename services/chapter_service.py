"""
==================================
MANGA GALLERY
CHAPTER SERVICE
==================================
"""

from database import db

from models.chapter import Chapter


class ChapterService:


    """
    ==============================
    GET ALL CHAPTERS
    ==============================
    """

    @staticmethod

    def get_all():

        return Chapter.query.all()


    """
    ==============================
    GET ONE CHAPTER
    ==============================
    """

    @staticmethod

    def get_by_id(

        chapter_id

    ):

        return Chapter.query.get(

            chapter_id

        )


    """
    ==============================
    SEARCH CHAPTER
    ==============================
    """

    @staticmethod

    def search(

        keyword

    ):

        return Chapter.query.filter(

            Chapter.title.ilike(

                f"%{keyword}%"

            )

        ).all()
        
    # ==================================
    # CREATE CHAPTER
    # ==================================


    @staticmethod

    def create(

        data

    ):

        chapter = Chapter(

            **data

        )

        db.session.add(

            chapter

        )

        db.session.commit()

        return chapter


    # ==================================
    # UPDATE CHAPTER
    # ==================================

    @staticmethod

    def update(

        chapter,

        data

    ):

        for key, value in data.items():

            setattr(

                chapter,

                key,

                value

            )

        db.session.commit()

        return chapter


    # ==================================
    # DELETE CHAPTER
    # ==================================

    @staticmethod

    def delete(

        chapter

    ):

        db.session.delete(

            chapter

        )

        db.session.commit()

        return True
        
    # ==================================
    # UPDATE VIEWS
    # ==================================


    @staticmethod

    def increment_views(

        chapter

    ):

        chapter.views += 1

        db.session.commit()

        return chapter


    # ==================================
    # UPDATE PAGES
    # ==================================

    @staticmethod

    def update_pages(

        chapter,

        pages

    ):

        chapter.pages = pages

        db.session.commit()

        return chapter


    # ==================================
    # UPDATE READING TIME
    # ==================================

    @staticmethod

    def update_reading_time(

        chapter,

        reading_time

    ):

        chapter.reading_time = reading_time

        db.session.commit()

        return chapter