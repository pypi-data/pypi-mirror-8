# -*- coding: utf-8 -*-
"""
    user

    Add the employee relation ship to nereid user

    :copyright: (c) 2012-2014 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
from datetime import datetime

from nereid import request, jsonify, login_required, route
from trytond.pool import Pool, PoolMeta
from trytond.model import fields

__all__ = ['NereidUser']
__metaclass__ = PoolMeta


class NereidUser:
    """
    Add employee
    """
    __name__ = "nereid.user"

    #: Allow the nereid user to be connected to an internal employee. This
    #: indicates that the user is an employee and not a regular participant
    employee = fields.Many2One('company.employee', 'Employee', select=True)

    member_of_projects = fields.One2Many(
        "project.work.member", "user", "Member of Projects"
    )

    def serialize(self, purpose=None):
        '''
        Serialize NereidUser and return a dictonary.
        '''
        result = super(NereidUser, self).serialize(purpose)
        result['image'] = {
            'url': self.get_profile_picture(size=20),
        }
        result['email'] = self.email
        result['employee'] = self.employee and self.employee.id or None
        result['permissions'] = [p.value for p in self.permissions]
        return result

    @classmethod
    @route("/me", methods=["GET", "POST"])
    @login_required
    def profile(cls):
        """
        User profile
        """
        if request.method == "GET" and request.is_xhr:
            user, = cls.browse([request.nereid_user.id])
            return jsonify(user.serialize())
        return super(NereidUser, cls).profile()

    def is_admin_of_project(self, project):
        """
        Check if user is admin member of the given project

        :param project: Active record of project
        """
        if request.nereid_user.has_permissions(['project.admin']):
            return True

        project = project.project

        assert project.type == 'project'

        for member in project.members:
            if member.user == self and member.role == 'admin':
                return True
        return False

    def hours_reported_today(self):
        """
        Returns the number of hours the nereid_user has done on the
        current date.

        """
        Timesheet = Pool().get('timesheet.line')

        if not self.employee:
            return 0.00

        current_date = datetime.utcnow().date()
        lines = Timesheet.search([
            ('date', '=', current_date),
            ('employee', '=', self.employee.id),
        ])

        return sum(map(lambda line: line.hours, lines))
