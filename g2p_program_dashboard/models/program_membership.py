# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, models

_logger = logging.getLogger(__name__)

# from odoo.http import request


class ProgramMembershipDashBoard(models.Model):
    _inherit = "g2p.program_membership"

    @api.model
    def count_beneficiaries(self, state=None):
        """
        Get total Beneficiaries
        """
        domain = [("program_id.company_id", "=", self.env.user.company_id.id)]
        if state is not None:
            domain += [("state", "in", state)]

        total = self.search_count(domain)
        return {"value": total}
