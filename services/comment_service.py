"""
==================================
MANGA GALLERY
COMMENT SERVICE
==================================
"""

from database import db

from models.comment import Comment


class CommentService:


    """
    ==============================
    GET ALL COMMENTS
    ==============================
    """

    @staticmethod

    def get_all():

        return Comment.query.all()


    """
    ==============================
    GET ONE COMMENT
    ==============================
    """

    @staticmethod

    def get_by_id(

        comment_id

    ):

        return Comment.query.get(

            comment_id

        )


    """
    ==============================
    SEARCH COMMENT
    ==============================
    """

    @staticmethod

    def search(

        keyword

    ):

        return Comment.query.filter(

            Comment.content.ilike(

                f"%{keyword}%"

            )

        ).all()
        
        """
==================================
CREATE COMMENT
==================================
"""

    @staticmethod

    def create(

        data

    ):

        comment = Comment(

            **data

        )

        db.session.add(

            comment

        )

        db.session.commit()

        return comment


    # ==================================
    # UPDATE COMMENT
    # ==================================

    @staticmethod

    def update(

        comment,

        data

    ):

        for key, value in data.items():

            setattr(

                comment,

                key,

                value

            )

        db.session.commit()

        return comment


    # ==================================
    # DELETE COMMENT
    # ==================================

    @staticmethod

    def delete(

        comment

    ):

        db.session.delete(

            comment

        )

        db.session.commit()

        return True
        
        """
==================================
UPDATE LIKES
==================================
"""

    @staticmethod

    def update_likes(

        comment,

        increment=True

    ):

        if increment:

            comment.likes += 1

        elif comment.likes > 0:

            comment.likes -= 1

        db.session.commit()

        return comment


    # ==================================
    # UPDATE REPORTS
    # ==================================

    @staticmethod

    def update_reports(

        comment

    ):

        comment.reports += 1

        db.session.commit()

        return comment


    # ==================================
    # COMMENT STATUS
    # ==================================

    @staticmethod

    def set_status(

        comment,

        status

    ):

        comment.status = status

        db.session.commit()

        return comment


    # ==================================
    # COMMENT STATISTICS
    # ==================================

    @staticmethod

    def statistics():

        total_comments = Comment.query.count()

        visible_comments = Comment.query.filter_by(

            status="visible"

        ).count()

        hidden_comments = Comment.query.filter(

            Comment.status != "visible"

        ).count()

        return {

            "total_comments": total_comments,

            "visible_comments": visible_comments,

            "hidden_comments": hidden_comments

        }