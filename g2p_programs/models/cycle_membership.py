#
# Copyright (c) 2022 Newlogic.
#
# This file is part of newlogic-g2p-erp.
# See https://github.com/newlogic/newlogic-g2p-erp/ for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from odoo import fields, models


class G2PCycleMembership(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _name = "g2p.cycle.membership"
    _description = "Cycle Membership"
    _order = "id desc"

    partner_id = fields.Many2one(
        "res.partner", "Registrant", help="A beneficiary", required=True, tracking=True
    )
    cycle_id = fields.Many2one(
        "g2p.cycle", "Cycle", help="A cycle", required=True, tracking=True
    )
    enrollment_date = fields.Date("Enrollment Date", tracking=True)
    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("enrolled", "Enrolled"),
            ("paused", "Paused"),
            ("exited", "Exited"),
        ],
        default="draft",
        copy=False,
    )

    def name_get(self):
        res = super(G2PCycleMembership, self).name_get()
        for rec in self:
            name = ""
            if rec.cycle_id:
                name += "[" + rec.cycle_id.name + "] "
            if rec.partner_id:
                name += rec.partner_id.name
            res.append((rec.id, name))
        return res

    def open_cycle_membership_form(self):
        return {
            "name": "Cycle Membership",
            "view_mode": "form",
            "res_model": "g2p.cycle.membership",
            "res_id": self.id,
            "view_id": self.env.ref("g2p_programs.view_cycle_membership_form").id,
            "type": "ir.actions.act_window",
            "target": "new",
        }
