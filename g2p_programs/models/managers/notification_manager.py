from odoo import api, fields, models


class BaseNotification(models.AbstractModel):
    """
    This component is used to notify beneficiaries of their enrollment and other events related to the program
    """

    _name = "g2p.program.notification.manager"

    _program = None

    def init_component(self, program):
        self._program = program

    def enrolled_in_program(self, program_memberships):
        return

    def cycle_started(self, cycle):
        return

    def cycle_ended(self, cycle):
        return
