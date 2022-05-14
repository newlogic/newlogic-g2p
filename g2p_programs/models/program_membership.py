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


class G2PProgramMembership(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _name = "g2p.program_membership"
    _description = "Program Membership"
    _order = "id desc"

    partner_id = fields.Many2one(
        "res.partner", "Registrant", help="A beneficiary", required=True, tracking=True
    )
    program_id = fields.Many2one(
        "g2p.program", "", help="A program", required=True, tracking=True
    )
    state = fields.Selection(
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
        res = super(G2PProgramMembership, self).name_get()
        for rec in self:
            name = ""
            if rec.program_id:
                name += "[" + rec.program_id.name + "] "
            if rec.partner_id:
                name += rec.partner_id.name
            res.append((rec.id, name))
        return res
