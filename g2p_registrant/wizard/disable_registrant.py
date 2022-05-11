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
