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


class EntitlementManager(models.Model):
    _name = "g2p.program.entitlement.manager"
    _description = "Entitlement Manager"
    _inherit = "g2p.manager.mixin"

    program_id = fields.Many2one("g2p.program", "Program")

    @api.model
    def _selection_manager_ref_id(self):
        selection = super()._selection_manager_ref_id()
        new_manager = ("g2p.program.entitlement.manager.default", "Default")
        if new_manager not in selection:
            selection.append(new_manager)
        return selection


class BaseEntitlementManager(models.AbstractModel):
    _name = "g2p.base.program.entitlement.manager"
    _description = "Base Entitlement Manager"

    name = fields.Char("Manager Name", required=True)
    program_id = fields.Many2one("g2p.program", string="Program", required=True)

    def prepare_vouchers(self, cycle, cycle_memberships):
        """
        This method is used to prepare the entitlement list of the beneficiaries.
        :param cycle: The cycle.
        :param cycle_memberships: The beneficiaries.
        :return:
        """
        raise NotImplementedError()

    def validate_vouchers(self, cycle, cycle_memberships):
        """
        This method is used to validate the entitlement list of the beneficiaries.
        :param cycle: The cycle.
        :param cycle_memberships: The beneficiaries.
        :return:
        """
        raise NotImplementedError()


class DefaultCashEntitlement(models.Model):
    _name = "g2p.program.entitlement.manager.default"
    _inherit = ["g2p.base.program.entitlement.manager", "g2p.manager.source.mixin"]
    _description = "Default Entitlement Manager"

    amount_per_cycle = fields.Monetary(
        currency_field="currency_id",
        group_operator="sum",
        default=0.0,
        string="Amount per cycle",
    )
    amount_per_individual_in_group = fields.Monetary(
        currency_field="currency_id",
        group_operator="sum",
        default=0.0,
        string="Amount per individual in group",
    )
    max_individual_in_group = fields.Integer(
        default=0,
        string="Maximum number of individual in group",
        help="0 means no limit",
    )

    currency_id = fields.Many2one(
        "res.currency", related="program_id.journal_id.currency_id", readonly=True
    )

    # Group able to validate the payment
    # Todo: Create a record rule for payment_validation_group
    voucher_validation_group_id = fields.Many2one(
        "res.groups", string="Payment Validation Group"
    )

    def prepare_vouchers(self, cycle, beneficiaries):
        # TODO: create a Voucher of `amount_per_cycle` for each member that do not have one yet for the cycle and
        benecifiaries_ids = beneficiaries.mapped("partner_id.id")
        benecifiaries_with_vouchers = (
            self.env["g2p.voucher"]
            .search(
                [("cycle_id", "=", cycle.id), ("partner_id", "in", benecifiaries_ids)]
            )
            .mapped("partner_id.id")
        )
        vouchers_to_create = [
            benecifiaries_id
            for benecifiaries_id in benecifiaries_ids
            if benecifiaries_id not in benecifiaries_with_vouchers
        ]

        voucher_start_validity = cycle.start_date
        voucher_end_validity = cycle.end_date
        voucher_currency = self.currency_id.id

        beneficiaries_with_vouchers_to_create = self.env["res.partner"].browse(
            vouchers_to_create
        )

        for beneficiary_id in beneficiaries_with_vouchers_to_create:
            self.env["g2p.voucher"].create(
                {
                    "cycle_id": cycle.id,
                    "partner_id": beneficiary_id.id,
                    "initial_amount": self._calculate_amount(beneficiary_id),
                    "currency_id": voucher_currency,
                    "state": "draft",
                    "is_cash_voucher": True,
                    "valid_from": voucher_start_validity,
                    "valid_until": voucher_end_validity,
                }
            )

    def _calculate_amount(self, beneficiary):
        total = self.amount_per_cycle
        if beneficiary.is_group:
            num_individuals = beneficiary.count_individuals()
            if (
                self.max_individual_in_group
                and num_individuals > self.max_individual_in_group
            ):
                num_individuals = self.max_individual_in_group
            total += self.amount_per_individual_in_group * num_individuals
        return total

    def validate_vouchers(self, cycle, cycle_memberships):
        # TODO: Change the status of the vouchers to `validated` for this members.
        # move the funds from the program's wallet to the wallet of each Beneficiary that are validated
        pass
