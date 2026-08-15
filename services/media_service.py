"""
==================================
MANGA GALLERY
MEDIA SERVICE
==================================
"""

from database import db

from models.media import Media


class MediaService:


    """
    ==============================
    GET ALL MEDIA
    ==============================
    """

    @staticmethod

    def get_all():

        return Media.query.all()


    """
    ==============================
    GET ONE MEDIA
    ==============================
    """

    @staticmethod

    def get_by_id(

        media_id

    ):

        return Media.query.get(

            media_id

        )


    """
    ==============================
    SEARCH MEDIA
    ==============================
    """

    @staticmethod

    def search(

        keyword

    ):

        return Media.query.filter(

            Media.filename.ilike(

                f"%{keyword}%"

            )

        ).all()
        
        """
==================================
UPLOAD MEDIA
==================================
"""

    @staticmethod

    def create(

        data

    ):

        media = Media(

            **data

        )

        db.session.add(

            media

        )

        db.session.commit()

        return media


    # ==================================
    # RENAME MEDIA
    # ==================================

    @staticmethod

    def rename(

        media,

        filename

    ):

        media.filename = filename

        db.session.commit()

        return media


    # ==================================
    # DELETE MEDIA
    # ==================================

    @staticmethod

    def delete(

        media

    ):

        db.session.delete(

            media

        )

        db.session.commit()

        return True
        
        """
==================================
DOWNLOAD MEDIA
==================================
"""

    @staticmethod

    def download(

        media

    ):

        return media.file_path


    # ==================================
    # MEDIA STATISTICS
    # ==================================

    @staticmethod

    def statistics():

        total_media = Media.query.count()

        total_size = db.session.query(

            db.func.sum(

                Media.file_size

            )

        ).scalar() or 0

        return {

            "total_media": total_media,

            "total_size": total_size

        }


    # ==================================
    # GET MEDIA BY TYPE
    # ==================================

    @staticmethod

    def get_by_type(

        file_type

    ):

        return Media.query.filter_by(

            file_type=file_type

        ).all()