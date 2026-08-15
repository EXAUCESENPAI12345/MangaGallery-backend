"""
==================================
MANGA GALLERY
NOTIFICATION SERVICE
==================================
"""

from database import db

from models.notification import Notification


class NotificationService:


    """
    ==============================
    GET ALL NOTIFICATIONS
    ==============================
    """

    @staticmethod

    def get_all():

        return Notification.query.all()


    """
    ==============================
    GET USER NOTIFICATIONS
    ==============================
    """

    @staticmethod

    def get_user_notifications(

        user_id

    ):

        return Notification.query.filter_by(

            user_id=user_id

        ).all()


    """
    ==============================
    GET ONE NOTIFICATION
    ==============================
    """

    @staticmethod

    def get_by_id(

        notification_id

    ):

        return Notification.query.get(

            notification_id

        )
        
        """
==================================
CREATE NOTIFICATION
==================================
"""

    @staticmethod

    def create(

        data

    ):

        notification = Notification(

            **data

        )

        db.session.add(

            notification

        )

        db.session.commit()

        return notification


    # ==================================
    # CREATE GLOBAL NOTIFICATION
    # ==================================

    @staticmethod

    def create_global(

        title,

        message,

        notification_type="info"

    ):

        notification = Notification(

            title=title,

            message=message,

            type=notification_type,

            is_global=True

        )

        db.session.add(

            notification

        )

        db.session.commit()

        return notification


    # ==================================
    # MARK AS READ
    # ==================================

    @staticmethod

    def mark_as_read(

        notification

    ):

        notification.is_read = True

        db.session.commit()

        return notification
        
        """
==================================
DELETE NOTIFICATION
==================================
"""

    @staticmethod

    def delete(

        notification

    ):

        db.session.delete(

            notification

        )

        db.session.commit()

        return True


    # ==================================
    # NOTIFICATION STATISTICS
    # ==================================

    @staticmethod

    def statistics():

        total_notifications = Notification.query.count()

        read_notifications = Notification.query.filter_by(

            is_read=True

        ).count()

        unread_notifications = Notification.query.filter_by(

            is_read=False

        ).count()

        global_notifications = Notification.query.filter_by(

            is_global=True

        ).count()

        return {

            "total_notifications": total_notifications,

            "read_notifications": read_notifications,

            "unread_notifications": unread_notifications,

            "global_notifications": global_notifications

        }


    # ==================================
    # UNREAD NOTIFICATIONS
    # ==================================

    @staticmethod

    def get_unread(

        user_id

    ):

        return Notification.query.filter_by(

            user_id=user_id,

            is_read=False

        ).all()