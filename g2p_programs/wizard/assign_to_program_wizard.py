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


class G2PAssignToProgramWizard(models.TransientModel):
    _name = "g2p.assign.program.wizard"
    _description = "Registrant Assign to Program Wizard"

    @api.model
    def default_get(self, fields):
        res = super(G2PAssignToProgramWizard, self).default_get(fields)
        _logger.info(
            "Assigning to Program Wizard with IDs: %s"
            % self.env.context.get("active_ids")
        )
        if self.env.context.get("active_ids"):
            reg_ids = []
            for rec in self.env.context.get("active_ids"):
                reg_ids.append([0, 0, {"partner_id": rec}])
            _logger.info("REG IDS: %s" % reg_ids)
            res["registrant_ids"] = reg_ids
        return res

    registrant_ids = fields.One2many(
        "g2p.assign.program.registrants",
        "program_id",
        string="Registrant",
        required=True,
    )
    program_id = fields.Many2one("g2p.program", "", help="A program", required=True)

    def assign_registrant(self):
        for rec in self.registrant_ids:
            curr_registrant = self.env["g2p.program_membership"].search(
                [
                    ("partner_id", "=", rec.partner_id.id),
                    ("program_id", "=", self.program_id.id),
                ]
            )
            if curr_registrant:
                rec.update({"state": "Conflict"})
            else:
                rec.update({"state": "Okay"})
                main_vals = {
                    "partner_id": rec.partner_id.id,
                    "program_id": self.program_id.id,
                }
                _logger.info("Assigning to Program Membership: %s" % main_vals)
                self.env["g2p.program_membership"].create(main_vals)

    def open_wizard(self):

        _logger.info("Registrant IDs: %s" % self.env.context.get("active_ids"))
        return {
            "name": "Assign to Program",
            "view_mode": "form",
            "res_model": "g2p.assign.program.wizard",
            "view_id": self.env.ref(
                "g2p_programs.assign_to_program_wizard_form_view"
            ).id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": self.env.context,
        }


class G2PAssignToProgramRegistrants(models.TransientModel):
    _name = "g2p.assign.program.registrants"
    _description = "Registrant Assign to Program"

    partner_id = fields.Many2one(
        "res.partner",
        "Registrant",
        help="A beneficiary",
        required=True,
        domain=[("is_registrant", "=", True)],
    )
    program_id = fields.Many2one(
        "g2p.assign.program.wizard",
        "Program Wizard",
        help="A program",
        required=True,
    )
    state = fields.Selection(
        [
            ("New", "New"),
            ("Okay", "Okay"),
            ("Conflict", "Conflict"),
            ("Assigned", "Assigned"),
        ],
        "Status",
        readonly=True,
        default="New",
    )
