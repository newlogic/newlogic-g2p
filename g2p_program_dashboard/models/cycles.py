# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.


from odoo import api, models

# from odoo.http import request


class CycleDashBoard(models.Model):
    _inherit = "g2p.cycle"

    @api.model
    def count_cycles(self, state=None):
        """
        Get total cycles per status
        """
        domain = [("company_id", "=", self.env.user.company_id.id)]
        if state is not None:
            domain += [("state", "in", state)]

        total = self.search_count(domain)
        return {"value": total}

    @api.model
    def get_cycle_ids(self, state=None):
        """
        Get ids of all cycles by state
        """
        domain = [("company_id", "=", self.env.user.company_id.id)]
        if state:
            domain += [("state", "in", state)]
        return self.search(domain).ids or None
