# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class G2PPhoneNumber(models.Model):
    _name = "g2p.phone.number"
    _description = "Phone Number"
    _order = "id desc"
    _rec_name = "phone_no"

    partner_id = fields.Many2one(
        "res.partner",
        "Registrant",
        required=True,
        domain=[("is_registrant", "=", True)],
    )
    phone_no = fields.Char("Phone Number", required=True)
    date_collected = fields.Date("Date Collected", default=fields.Date.today)
    disabled = fields.Datetime("Date Disabled")
    disabled_by = fields.Many2one("res.users", "Disabled by")

    def disable_phone(self):
        for rec in self:
            if not rec.disabled:
                rec.update(
                    {
                        "disabled": fields.Datetime.now(),
                        "disabled_by": self.env.user,
                    }
                )

    def enable_phone(self):
        for rec in self:
            if rec.disabled:
                rec.update(
                    {
                        "disabled": None,
                        "disabled_by": None,
                    }
                )
