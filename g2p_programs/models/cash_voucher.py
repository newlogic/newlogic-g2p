#################################################################################
#   Copyright 2022 Newlogic
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#################################################################################
from odoo import _, api, fields, models


class G2PCashVoucher(models.Model):
    _name = "g2p.cash_voucher"
    _description = "Cash voucher"
    _order = "id desc"

    voucher_id = fields.Many2one(
        "g2p.voucher", help="If empty, all users can use it", tracking=True
    )  # one to one

    currency_id = fields.Many2one(
        "res.currency",
        readonly=True,
        related="voucher_id.company_id.currency_id",
        tracking=True,
    )
    initial_amount = fields.Monetary(required=True, currency_field="currency_id")
    balance = fields.Monetary(compute="_compute_balance")  # in company currency
    # TODO: implement transactions against this voucher

    _sql_constraints = [
        (
            "check_amount",
            "CHECK(initial_amount >= 0)",
            "The initial amount must be positive.",
        )
    ]

    def _compute_name(self):
        for record in self:
            record.name = _("Cash voucher #%s", record.id)

    @api.depends("initial_amount")
    def _compute_balance(self):
        for record in self:
            record.balance = record.initial_amount
