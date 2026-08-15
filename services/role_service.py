"""
==================================
MANGA GALLERY
ROLE SERVICE
==================================
"""

from database import db

from models.role import Role


class RoleService:


    """
    ==============================
    GET ALL ROLES
    ==============================
    """

    @staticmethod

    def get_all():

        return Role.query.all()


    """
    ==============================
    GET ONE ROLE
    ==============================
    """

    @staticmethod

    def get_by_id(

        role_id

    ):

        return Role.query.get(

            role_id

        )


    """
    ==============================
    SEARCH ROLE
    ==============================
    """

    @staticmethod

    def search(

        keyword

    ):

        return Role.query.filter(

            Role.name.ilike(

                f"%{keyword}%"

            )

        ).all()
        
        """
==================================
CREATE ROLE
==================================
"""

    @staticmethod

    def create(

        data

    ):

        role = Role(

            **data

        )

        db.session.add(

            role

        )

        db.session.commit()

        return role


    # ==================================
    # UPDATE ROLE
    # ==================================

    @staticmethod

    def update(

        role,

        data

    ):

        for key, value in data.items():

            setattr(

                role,

                key,

                value

            )

        db.session.commit()

        return role


    # ==================================
    # DELETE ROLE
    # ==================================

    @staticmethod

    def delete(

        role

    ):

        db.session.delete(

            role

        )

        db.session.commit()

        return True
        
        """
==================================
ASSIGN ROLE
==================================
"""

    @staticmethod

    def assign_role(

        user,

        role_id

    ):

        user.role_id = role_id

        db.session.commit()

        return user


    # ==================================
    # UPDATE PERMISSIONS
    # ==================================

    @staticmethod

    def update_permissions(

        role,

        permissions

    ):

        role.permissions = permissions

        db.session.commit()

        return role


    # ==================================
    # ROLE STATISTICS
    # ==================================

    @staticmethod

    def statistics():

        total_roles = Role.query.count()

        active_roles = Role.query.filter_by(

            is_active=True

        ).count()

        system_roles = Role.query.filter_by(

            is_system=True

        ).count()

        return {

            "total_roles": total_roles,

            "active_roles": active_roles,

            "system_roles": system_roles

        }