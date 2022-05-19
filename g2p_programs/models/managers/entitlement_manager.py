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
        currency_field="currency_id", group_operator="sum"
    )
    currency_id = fields.Many2one("res.currency")

    # Group able to validate the payment
    # Todo: Create a record rule for payment_validation_group
    voucher_validation_group_id = fields.Many2one(
        "res.groups", string="Payment Validation Group"
    )

    # TODO: JJ - Think about how we could simply allow to have an amount per individual of a group with a maximum amount.

    def prepare_vouchers(self, cycle, cycle_memberships):
        # TODO: create a Voucher of `amount_per_cycle` for each member that do not have one yet for the cycle and
        pass

    def validate_vouchers(self, cycle, cycle_memberships):
        # TODO: Change the status of the vouchers to `validated` for this members.
        # move the funds from the program's wallet to the wallet of each Beneficiary that are validated
        pass
