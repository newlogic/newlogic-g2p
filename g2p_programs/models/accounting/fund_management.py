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
from odoo.exceptions import UserError  # , RedirectWarning, ValidationError, AccessError


class ProgramFundManagement(models.Model):
    _name = "g2p.program.fund"
    _description = "Program Fund Entries"
    _inherit = ["mail.thread"]
    _order = "id desc"

    name = fields.Char(
        "Reference Number", required=True, default="Draft", tracking=True
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, tracking=True
    )
    program_id = fields.Many2one("g2p.program", "Program", required=True, tracking=True)
    journal_id = fields.Many2one(
        "account.journal",
        "Disbursement Journal",
        related="program_id.journal_id",
        store=True,
    )
    account_move_id = fields.Many2one("account.move", "Journal Entry")
    amount = fields.Monetary(required=True, currency_field="currency_id", tracking=True)
    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id
        and self.env.user.company_id.currency_id.id
        or None,
        tracking=True,
    )
    remarks = fields.Text("Remarks", tracking=True)
    date_posted = fields.Date(
        "Date Posted", required=True, default=fields.Date.today, tracking=True
    )
    state = fields.Selection(
        [("draft", "Draft"), ("posted", "Posted"), ("cancelled", "Cancelled")],
        "Status",
        readonly=True,
        default="draft",
        tracking=True,
    )

    @api.ondelete(at_uninstall=False)
    def _unlink_fund(self):
        if self.state == "posted":
            raise UserError(_("This fund is already posted and cannot be deleted."))

    def post_fund(self):
        for rec in self:
            if rec.state == "draft":
                vals = {"state": "posted", "date_posted": fields.Date.today()}
                if rec.name in ("Draft", None):
                    vals.update(
                        {
                            "name": self.env["ir.sequence"].next_by_code(
                                "program.fund.ref.num"
                            )
                            or "NONE"
                        }
                    )
                # TODO: Generate journal entry
                rec.update(vals)
                return {
                    "effect": {
                        "fadeout": "slow",
                        "message": "This fund is now posted!",
                        "type": "rainbow_man",
                    }
                }
            else:
                message = _("Only draft program funds can be posted.")
                kind = "error"
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": _("Program Fund"),
                        "message": message,
                        "sticky": True,
                        "type": kind,
                    },
                }

    def cancel_fund(self):
        for rec in self:
            if rec.state == "draft":
                rec.update({"state": "cancelled"})
            else:
                message = _("Only draft program funds can be cancelled.")
                kind = "error"
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": _("Program Fund"),
                        "message": message,
                        "sticky": True,
                        "type": kind,
                    },
                }

    def reset_draft(self):
        for rec in self:
            if rec.state == "cancelled":
                rec.update({"state": "draft"})
            else:
                message = _("Only cancelled program funds can be reset to draft.")
                kind = "danger"
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": _("Program Fund"),
                        "message": message,
                        "sticky": True,
                        "type": kind,  # types: success,warning,danger,info
                    },
                }