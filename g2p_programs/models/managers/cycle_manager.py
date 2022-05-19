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

class CycleManager(models.Model):
    _name = "g2p.cycle.manager"
    _description = "Cycle Manager"
    _inherit = "g2p.manager.mixin"

    program_id = fields.Many2one("g2p.program", "Program")

    @api.model
    def _selection_manager_ref_id(self):
        selection = super()._selection_manager_ref_id()
        new_manager = ("g2p.cycle.manager.default", "Default")
        if new_manager not in selection:
            selection.append(new_manager)
        return selection

class BaseCycleManager(models.AbstractModel):
    _name = "g2p.base.cycle.manager"
    _description = "Base Cycle Manager"

    name = fields.Char("Manager Name", required=True)
    program_id = fields.Many2one("g2p.program", string="Program", required=True)
    cycle_id = fields.Many2one("g2p.cycle", string="Cycle", required=True)

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

    def new_cycle(self, new_start_date):
        """
        Create a new cycle for the program
        """
        raise NotImplementedError()

    def on_start_date_change(self, start_date):
        """
        Hook for when the start date change
        """
        raise NotImplementedError()


class DefaultCycleManager(models.Model):
    _name = "g2p.cycle.manager.default"
    _inherit = ["g2p.base.cycle.manager","g2p.manager.source.mixin"]
    _description = "Default Cycle Manager"

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
