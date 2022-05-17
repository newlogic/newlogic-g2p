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


class BaseCycleManager(models.AbstractModel):
    _name = "g2p.cycle.manager"

    program_id = fields.Many2one("g2p.program", string="Program", editable=False)
    cycle_id = fields.Many2one("g2p.cycle", string="Cycle", editable=False)

    def next_cycle(self):
        """
        Return the next cycle of the program if any
        Returns:
            cycle: the next cycle of the program
        """
        #  TODO: Get the next cycle of the program base ont he sequence number
        raise NotImplementedError()

    def previous_cycle(self):
        """
        Return the previous cycle of the program if any
        Returns:
            cycle: the previous cycle of the program
        """
        #  TODO: Get the previous cycle of the program base ont he sequence number
        raise NotImplementedError()

    def check_eligibility(self):
        """
        Validate the eligibility of each beneficiaries for the cycle
        """
        raise NotImplementedError()

    def prepare_vouchers(self):
        """
        Prepare the entitlements for the cycle
        """
        raise NotImplementedError()

    def validate_vouchers(self, cycle_memberships):
        """
        Validate the entitlements for the cycle
        """
        raise NotImplementedError()


class DefaultCycleManager(models.Model):
    _name = "g2p.cycle.manager.default"

    _inherit = "g2p.cycle.manager"

    def check_eligibility(self):
        #  TODO: call the program's eligibility manager and check if the beneficiary is still eligible
        pass

    def prepare_vouchers(self):
        # TODO: call the program's entitlement manager and prepare the entitlements
        # TODO: Use a Job attached to the cycle
        pass

    def validate_vouchers(self, cycle_memberships):
        # TODO: call the program's entitlement manager and validate the entitlements
        # TODO: Use a Job attached to the cycle
        pass
