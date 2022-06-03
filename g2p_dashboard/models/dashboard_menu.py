# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class DashBoardMenu(models.Model):
    _inherit = "dashboard.menu"

    sequence = fields.Integer("Sequence", default=1)

    @api.model
    def create(self, vals):
        """This code is to create menu"""
        values = {
            "name": vals["name"],
            "tag": "dynamic_dashboard",
        }
        action_id = self.env["ir.actions.client"].create(values)
        vals["client_action"] = action_id.id
        menu_id = self.env["ir.ui.menu"].create(
            {
                "name": vals["name"],
                "parent_id": vals["menu_id"],
                "sequence": vals["sequence"],
                "action": "ir.actions.client,%d" % (action_id.id,),
            }
        )
        vals["menu_id"] = menu_id.id
        return super(DashBoardMenu, self).create(vals)
