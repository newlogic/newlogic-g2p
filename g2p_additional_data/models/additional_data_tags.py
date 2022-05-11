from random import randint

from odoo import fields, models


class G2PAdditionalDataTags(models.Model):
    _name = "g2p.additional.data.tags"
    _description = "Tags"
    _order = "id desc"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Name")
    color = fields.Integer(string="Color", default=_get_default_color)

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Tag name already exists!"),
    ]
