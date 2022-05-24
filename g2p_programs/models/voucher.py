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
        "res.partner", "Registrant", help="A beneficiary", required=True, tracking=True
    )
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    cycle_id = fields.Many2one("g2p.cycle", required=True, tracking=True)

    valid_from = fields.Date(required=False, tracking=True)
    valid_until = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.today(), years=1)
    )

    is_cash_voucher = fields.Boolean("Cash Voucher", default=False)
    currency_id = fields.Many2one("res.currency")
    initial_amount = fields.Monetary(required=True, currency_field="currency_id")
    balance = fields.Monetary(compute="_compute_balance")  # in company currency
    # TODO: implement transactions against this voucher

    # state = fields.Selection(
    #    selection=[('draft', 'Draft'), ('valid', 'Valid'), ('expired', 'Expired')],
    #    default='draft',
    #    copy=False
    # )

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

    @api.autovacuum
    def _gc_mark_expired_voucher(self):
        self.env["g2p.voucher"].search(
            ["&", ("state", "=", "approved"), ("valid_until", "<", fields.Date.today())]
        ).write({"state": "expired"})

    def can_be_used(self):
        # expired state are computed once a day, so can be not synchro
        return self.state == "approved" and self.valid_until >= fields.Date.today()

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
