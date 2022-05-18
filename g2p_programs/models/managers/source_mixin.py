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
from odoo import api, fields, models


class ManagerSourceMixin(models.AbstractModel):
    """Manager Data Source mixin.
    """

    _name = "g2p.manager.source.mixin"
    _description = "Manager Data Source Mixin"

    @api.model
    def create(self, vals):
        """Override to update reference to source on the manager."""
        res = super().create(vals)
        if self.env.context.get("active_model"):
            # update reference on manager
            self.env[self.env.context["active_model"]].browse(
                self.env.context["active_id"]
            ).manager_id = res.id
        return res

    def get_manager_view_id(self):
        """Retrieve form view."""
        return (
            self.env["ir.ui.view"]
            .search([("model", "=", self._name), ("type", "=", "form")], limit=1)
            .id
        )
