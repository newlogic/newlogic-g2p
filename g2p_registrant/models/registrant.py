#################################################################################
#   Copyright 2022 Newlogic
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#################################################################################

from odoo import fields, models


class G2PRegistrant(models.Model):
    _inherit = "res.partner"

    # Custom Fields
    address = fields.Text("Address", tracking=True)
    addl_fields = fields.One2many(
        "g2p.reg.attribute.value", "partner_id", "Additional Fields", tracking=True
    )
    disabled = fields.Datetime("Date Disabled", tracking=True)
    disabled_reason = fields.Text("Reason for disabling", tracking=True)
    disabled_by = fields.Many2one("res.users", "Disabled by", tracking=True)
    # Tag (exist in res.partner: category_id)

    reg_ids = fields.One2many("g2p.reg.id", "registrant", "Registrant IDs")
    is_registrant = fields.Boolean("Registrant")
    is_group = fields.Boolean("Group")

    name = fields.Char(index=True, translate=True)

    def enable_registrant(self):
        for rec in self:
            if rec.disabled:
                rec.update(
                    {
                        "disabled": None,
                        "disabled_by": None,
                        "disabled_reason": None,
                    }
                )
