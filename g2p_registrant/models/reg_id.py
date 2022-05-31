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

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class G2PRegistrantID(models.Model):
    _name = "g2p.reg.id"
    _description = "Registrant ID"
    _order = "id desc"

    registrant = fields.Many2one(
        "res.partner",
        "Registrant",
        required=True,
        domain=[("is_registrant", "=", True)],
    )
    id_type = fields.Many2one("g2p.id.type", "ID Type", required=True)
    value = fields.Char("Value", size=100)

    expiry_date = fields.Datetime("Expiry Date", tracking=True)

    def name_get(self):
        res = super(G2PRegistrantID, self).name_get()
        for rec in self:
            name = ""
            if rec.registrant:
                name = rec.registrant.name
            res.append((rec.id, name))
        return res

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        if name:
            args = [("registrant", operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


class G2PIDType(models.Model):
    _name = "g2p.id.type"
    _description = "ID Type"
    _order = "id desc"

    name = fields.Char("Name")

    def unlink(self):
        for rec in self:
            external_identifier = self.env["ir.model.data"].search(
                [("res_id", "=", rec.id), ("model", "=", "g2p.id.type")]
            )
            if external_identifier.name == "id_type_idpass":
                raise ValidationError(_("Can't delete default ID Type"))
            else:
                return super(G2PIDType, self).unlink()

    def write(self, vals):
        external_identifier = self.env["ir.model.data"].search(
            [("res_id", "=", self.id), ("model", "=", "g2p.id.type")]
        )
        if external_identifier.name == "id_type_idpass":
            raise ValidationError(_("Can't edit default ID Type"))
        else:
            return super(G2PIDType, self).write(vals)
