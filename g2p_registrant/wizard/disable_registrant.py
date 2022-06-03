# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class G2PDisableRegistrantWiz(models.TransientModel):
    _name = "g2p.disable.registrant.wizard"
    _description = "Disable Registrant Wizard"

    @api.model
    def default_get(self, fields):
        res = super(G2PDisableRegistrantWiz, self).default_get(fields)
        if self.env.context.get("active_id"):
            res["partner_id"] = self.env.context["active_id"]
        return res

    partner_id = fields.Many2one("res.partner", "Registrant", required=True)
    disabled_reason = fields.Text("Reason for disabling", required=True)

    def disable_registrant(self):
        for rec in self:
            rec.partner_id.update(
                {
                    "disabled": fields.Datetime.now(),
                    "disabled_reason": rec.disabled_reason,
                    "disabled_by": self.env.user,
                }
            )
