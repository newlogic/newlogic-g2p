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
from uuid import uuid4

from odoo import _, api, fields, models


class G2PVoucher(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _name = "g2p.voucher"
    _description = "Voucher"
    _order = "id desc"
    _check_company_auto = True

    @api.model
    def _generate_code(self):
        return str(uuid4())[4:-8][3:]

    name = fields.Char(compute="_compute_name")
    code = fields.Char(
        default=lambda x: x._generate_code(), required=True, readonly=True, copy=False
    )

    partner_id = fields.Many2one(
        "res.partner",
        "Registrant",
        help="A beneficiary",
        required=True,
        domain=[("is_registrant", "=", True)],
    )
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    cycle_id = fields.Many2one("g2p.cycle", required=True)

    valid_from = fields.Date(required=False)
    valid_until = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.today(), years=1)
    )

    is_cash_voucher = fields.Boolean("Cash Voucher", default=False)
    currency_id = fields.Many2one(
        "res.currency", readonly=True, related="journal_id.currency_id"
    )
    initial_amount = fields.Monetary(required=True, currency_field="currency_id")
    balance = fields.Monetary(compute="_compute_balance")  # in company currency
    # TODO: implement transactions against this voucher

    journal_id = fields.Many2one(
        "account.journal",
        "Disbursement Journal",
        store=True,
        compute="_compute_journal_id",
    )
    disbursement_id = fields.Many2one("account.payment", "Disbursement Journal Entry")

    date_approved = fields.Date("Date Approved")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending_validation", "Pending Validation"),
            ("approved", "Approved"),
            ("trans2FSP", "Transferred to FSP"),
            ("rdpd2ben", "Redeemed/Paid to Beneficiary"),
            ("rejected1", "Rejected: Beneficiary didn't want the voucher"),
            ("rejected2", "Rejected: Beneficiary account does not exist"),
            ("rejected3", "Rejected: Other reason"),
            ("cancelled", "Cancelled"),
            ("expired", "Expired"),
        ],
        "Status",
        default="draft",
        copy=False,
    )

    _sql_constraints = [
        ("unique_voucher_code", "UNIQUE(code)", "The voucher code must be unique."),
    ]

    def _compute_name(self):
        for record in self:
            name = _("Voucher")
            if record.is_cash_voucher:
                name += " Cash [" + str(record.initial_amount) + "]"
            record.name = name

    @api.depends("initial_amount")
    def _compute_balance(self):
        for record in self:
            record.balance = record.initial_amount

    @api.depends("cycle_id.program_id.journal_id")
    def _compute_journal_id(self):
        for record in self:
            record.journal_id = (
                record.cycle_id
                and record.cycle_id.program_id
                and record.cycle_id.program_id.journal_id
                and record.cycle_id.program_id.journal_id.id
                or None
            )

    @api.autovacuum
    def _gc_mark_expired_voucher(self):
        self.env["g2p.voucher"].search(
            ["&", ("state", "=", "approved"), ("valid_until", "<", fields.Date.today())]
        ).write({"state": "expired"})

    def can_be_used(self):
        # expired state are computed once a day, so can be not synchro
        return self.state == "approved" and self.valid_until >= fields.Date.today()

    def approve_voucher(self):
        for rec in self:
            if rec.state in ("draft", "pending_validation"):
                # Prepare journal entry (account.move) via account.payment
                payment = {
                    "partner_id": rec.partner_id.id,
                    "payment_type": "outbound",
                    "amount": rec.initial_amount,
                    "currency_id": rec.journal_id.currency_id.id,
                    "journal_id": rec.journal_id.id,
                    "partner_type": "supplier",
                }
                new_payment = self.env["account.payment"].create(payment)
                rec.update(
                    {
                        "disbursement_id": new_payment.id,
                        "state": "approved",
                        "date_approved": fields.Date.today(),
                    }
                )
            else:
                message = _("The voucher must be in 'pending validation' state.")
                kind = "danger"
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": _("Voucher"),
                        "message": message,
                        "sticky": True,
                        "type": kind,
                    },
                }

    def open_voucher_form(self):
        return {
            "name": "Voucher",
            "view_mode": "form",
            "res_model": "g2p.voucher",
            "res_id": self.id,
            "view_id": self.env.ref("g2p_programs.view_voucher_form").id,
            "type": "ir.actions.act_window",
            "target": "new",
        }

    def open_disb_form(self):
        for rec in self:
            if rec.disbursement_id:
                res_id = rec.disbursement_id.id
                return {
                    "name": "Disbursement",
                    "view_mode": "form",
                    "res_model": "account.payment",
                    "res_id": res_id,
                    "view_id": self.env.ref("account.view_account_payment_form").id,
                    "type": "ir.actions.act_window",
                    "target": "current",
                }
