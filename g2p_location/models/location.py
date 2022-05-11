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


class G2PLocation(models.Model):
    _name = "g2p.location"
    _description = "Location"
    _order = "id desc"

    parent_id = fields.Many2one("g2p.location", "Parent")
    name = fields.Char("Name", required=True, translate=True)
    code = fields.Char("Code")
    altnames = fields.Char("Alternate Name")
    level = fields.Integer("Level")
    child_ids = fields.One2many(
        "g2p.location", "id", "Child", compute="_compute_get_childs"
    )

    def _compute_get_childs(self):
        for rec in self:
            child_ids = self.env["g2p.location"].search([("parent_id", "=", rec.id)])
            rec.child_ids = child_ids
