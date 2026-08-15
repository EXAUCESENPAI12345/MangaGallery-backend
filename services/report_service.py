"""
==================================
MANGA GALLERY
REPORT SERVICE
==================================
"""

from database import db

from models.report import Report


class ReportService:


    """
    ==============================
    GET ALL REPORTS
    ==============================
    """

    @staticmethod

    def get_all():

        return Report.query.all()


    """
    ==============================
    GET ONE REPORT
    ==============================
    """

    @staticmethod

    def get_by_id(

        report_id

    ):

        return Report.query.get(

            report_id

        )


    """
    ==============================
    SEARCH REPORT
    ==============================
    """

    @staticmethod

    def search(

        keyword

    ):

        return Report.query.filter(

            Report.reason.ilike(

                f"%{keyword}%"

            )

        ).all()
        
        """
==================================
APPROVE REPORT
==================================
"""

    @staticmethod

    def approve(

        report,

        moderator_id,

        note=None

    ):

        report.status = "approved"

        report.moderator_id = moderator_id

        report.moderator_note = note

        db.session.commit()

        return report


    # ==================================
    # REJECT REPORT
    # ==================================

    @staticmethod

    def reject(

        report,

        moderator_id,

        note=None

    ):

        report.status = "rejected"

        report.moderator_id = moderator_id

        report.moderator_note = note

        db.session.commit()

        return report


    # ==================================
    # DELETE REPORT
    # ==================================

    @staticmethod

    def delete(

        report

    ):

        db.session.delete(

            report

        )

        db.session.commit()

        return True
        
        """
==================================
REPORT STATISTICS
==================================
"""

    @staticmethod

    def statistics():

        total_reports = Report.query.count()

        pending_reports = Report.query.filter_by(

            status="pending"

        ).count()

        approved_reports = Report.query.filter_by(

            status="approved"

        ).count()

        rejected_reports = Report.query.filter_by(

            status="rejected"

        ).count()

        return {

            "total_reports": total_reports,

            "pending_reports": pending_reports,

            "approved_reports": approved_reports,

            "rejected_reports": rejected_reports

        }


    # ==================================
    # COUNT REPORTS
    # ==================================

    @staticmethod

    def count():

        return Report.query.count()


    # ==================================
    # GET PENDING REPORTS
    # ==================================

    @staticmethod

    def get_pending():

        return Report.query.filter_by(

            status="pending"

        ).all()