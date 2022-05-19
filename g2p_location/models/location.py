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
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class G2PLocation(models.Model):
    _name = "g2p.location"
    _description = "Location"
    _order = "id desc"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    parent_id = fields.Many2one("g2p.location", "Parent")
    complete_name = fields.Char(
        "Name", compute="_compute_complete_name", recursive=True, store=True
    )
    name = fields.Char("Name", required=True, translate=True)
    parent_path = fields.Char(index=True)
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

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for location in self:
            if location.parent_id:
                location.complete_name = "%s > %s" % (
                    location.parent_id.complete_name,
                    location.name,
                )
            else:
                location.complete_name = location.name

    @api.model
    def create(self, vals):
        Location = super(G2PLocation, self).create(vals)
        _logger.info("Location ID: %s" % Location.id)
        Languages = self.env["res.lang"].search([("active", "=", True)])
        vals_list = []
        for lang_code in Languages:
            vals_list.append(
                {
                    "name": "g2p.location,name",
                    "lang": lang_code.code,
                    "res_id": Location.id,
                    "src": Location.name,
                    "value": None,
                    "state": "to_translate",
                    "type": "model",
                }
            )

        self.env["ir.translation"]._upsert_translations(vals_list)
        return Location
