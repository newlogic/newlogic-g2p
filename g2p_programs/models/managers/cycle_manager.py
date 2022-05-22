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
import logging
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


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
    # cycle_id = fields.Many2one("g2p.cycle", string="Cycle", required=True)

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

    def new_cycle(self, name, new_start_date):
        """
        Create a new cycle for the program
        """
        raise NotImplementedError()

    def add_beneficiaries(self, cycle, beneficiaries, status="draft"):
        """
        Add beneficiaries to the cycle
        """
        raise NotImplementedError()

    def on_start_date_change(self, start_date):
        """
        Hook for when the start date change
        """
        raise NotImplementedError()


class DefaultCycleManager(models.Model):
    _name = "g2p.cycle.manager.default"
    _inherit = ["g2p.base.cycle.manager", "g2p.manager.source.mixin"]
    _description = "Default Cycle Manager"

    cycle_duration = fields.Integer("Cycle Duration", required=True)

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

    def new_cycle(self, name, new_start_date):
        _logger.info("Creating new cycle for program %s", self.program_id.name)
        _logger.info("New start date: %s", new_start_date)
        for rec in self:
            cycle = self.env["g2p.cycle"].create(
                {
                    "program_id": rec.program_id.id,
                    "name": name,
                    "state": "draft",
                    "sequence": 1,
                    "start_date": new_start_date,
                    "end_date": new_start_date + timedelta(days=rec.cycle_duration),
                }
            )
            _logger.info("New cycle created: %s", cycle.name)
            return cycle

    def copy_beneficiaries_from_program(self, cycle, status="enrolled"):
        for rec in self:
            if cycle.state not in [cycle.STATE_DRAFT, cycle.STATE_ACTIVE]:
                raise ValidationError(_("The Cycle is not in Draft or Active Mode"))
            beneficiary_ids = rec.program_id.get_beneficiaries(["enrolled"]).mapped(
                "partner_id.id"
            )
            rec.add_beneficiaries(cycle, beneficiary_ids, status)

    def add_beneficiaries(self, cycle, beneficiaries, status="draft"):
        """
        Add beneficiaries to the cycle
        """
        _logger.info("Adding beneficiaries to the cycle %s", cycle.name)
        _logger.info("Beneficiaries: %s", beneficiaries)

        existing_ids = cycle.cycle_membership_ids.mapped("partner_id.id")
        new_beneficiaries = []
        for r in beneficiaries:
            if r not in existing_ids:
                new_beneficiaries.append(
                    [
                        0,
                        0,
                        {
                            "partner_id": r,
                            "enrollment_date": fields.Date.today(),
                            "status": status,
                        },
                    ]
                )
        if new_beneficiaries:
            cycle.update({"cycle_membership_ids": new_beneficiaries})
            return True
        else:
            return False
