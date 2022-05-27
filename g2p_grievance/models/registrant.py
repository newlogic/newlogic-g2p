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


class G2PGrievanceRegistrant(models.Model):
    _inherit = "res.partner"

    def open_ticket_form(self):
        return {
            "name": "Create Ticket",
            "view_mode": "form",
            "res_model": "helpdesk.ticket",
            "view_id": self.env.ref("helpdesk_mgmt.ticket_view_form").id,
            "type": "ir.actions.act_window",
            "target": "current",
            "context": {"default_partner_id": self.id},
        }

    ticket_ids = fields.One2many("helpdesk.ticket", "partner_id", "Tickets")
