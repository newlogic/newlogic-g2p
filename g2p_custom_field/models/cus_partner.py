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

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class G2PResPartner(models.Model):
    _inherit = "res.partner"

    ui_view_id = fields.Many2one("ir.ui.view", string="UI View")

    def custom_view_create(self, inherit_id, arch_base):
        custom_view_id = (
            self.env["ir.ui.view"]
            .sudo()
            .create(
                {
                    "name": "individuals.inherit.fields",
                    "xml_id": "individuals.inherit.fields",
                    "type": "form",
                    "model": "res.partner",
                    "mode": "extension",
                    "inherit_id": inherit_id.id,
                    "arch_base": arch_base,
                    "active": True,
                }
            )
        )
        _logger.debug(f"Model trigger create: {custom_view_id}")
        return custom_view_id

    def custom_form_view(self):
        inherit_id = self.env.ref("g2p_registrant.view_individuals_form")
        model_id = self.env["ir.model.fields"].search(
            [("model_id", "=", "res.partner"), ("state", "=", "manual")]
        )

        arch_base = _(
            '<?xml version="1.0"?>'
            "<data>"
            '<page name="custom" position="inside">'
            '<group col="4" colspan="4">'
        )

        for rec in model_id:
            arch_base += f'<field name="{rec.name}"/>'

        arch_base += "</group></page></data>"

        _logger.debug(f"Model: {model_id}")
        _logger.debug(f"Model: {arch_base}")

        if not self.ui_view_id:
            custom_view_id = self.custom_view_create(inherit_id, arch_base)
            self.ui_view_id = custom_view_id

        else:
            self.ui_view_id.unlink()
            custom_view_id = self.custom_view_create(inherit_id, arch_base)
            self.ui_view_id = custom_view_id

        _logger.debug(f"Model: {str(self._inherit[0])}")
        return {"type": "ir.actions.client", "tag": "reload"}
