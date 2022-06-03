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


class ManagerMixin(models.AbstractModel):
    """Manager mixin."""

    _name = "g2p.manager.mixin"
    _description = "Manager Mixin"

    manager_id = fields.Integer("Manager ID")
    manager_ref_id = fields.Reference(
        string="Manager", selection="_selection_manager_ref_id", required=True
    )

    @api.model
    def _selection_manager_ref_id(self):
        return []

    def open_manager_form(self):
        self.ensure_one()
        if self.manager_ref_id:
            # Get the res_model and res_id from the manager_ref_id (reference field)
            manager_ref_id = str(self.manager_ref_id)
            s = manager_ref_id.find("(")
            res_model = manager_ref_id[:s]
            res_id = self.manager_ref_id.id
            if res_id:
                action = self.env[res_model].get_formview_action()
                action.update(
                    {
                        "views": [(self.env[res_model].get_manager_view_id(), "form")],
                        "res_id": res_id,
                        "target": "new",
                        "context": self.env.context,
                        "flags": {"mode": "readonly"},
                    }
                )
                return action

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "ERROR!",
                "message": "The Manager field must be filled-up.",
                "sticky": False,
                "type": "danger",
            },
        }
