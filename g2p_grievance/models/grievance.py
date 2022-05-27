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


class G2PGrievance(models.Model):
    _inherit = "helpdesk.ticket"

    program_id = fields.Many2one("g2p.program", "Program", tracking=True)
    cycle_id = fields.Many2one("g2p.cycle", "Cycle", tracking=True)

    @api.onchange("partner_id")
    def _get_programs(self):
        programs = self.env["g2p.program_membership"].search(
            [
                ("partner_id", "=", self.partner_id.id),
                ("state", "=", "enrolled"),
            ]
        )
        vals = []
        if programs:
            for line in programs:
                vals.append(line.program_id.id)
        res = {}
        res["domain"] = {"program_id": [("id", "in", vals)]}
        return res

    @api.onchange("program_id")
    def _get_cycle(self):
        cycle = self.env["g2p.cycle.membership"].search(
            [
                ("partner_id", "=", self.partner_id.id),
                ("state", "=", "enrolled"),
            ]
        )
        vals = []
        if cycle:
            for line in cycle:
                if line.cycle_id.program_id.id == self.program_id.id:
                    vals.append(line.cycle_id.id)
        res = {}
        res["domain"] = {"cycle_id": [("id", "in", vals)]}
        return res
