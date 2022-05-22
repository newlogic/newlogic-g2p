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

from odoo import api, fields, models

from . import constants

_logger = logging.getLogger(__name__)


class G2PCycle(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin", "g2p.job.mixin"]
    _name = "g2p.cycle"
    _description = "Cycle"
    _order = "id desc"
    _check_company_auto = True

    STATE_DRAFT = constants.STATE_DRAFT
    STATE_ACTIVE = constants.STATE_ACTIVE
    STATE_ENDED = constants.STATE_ENDED

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, tracking=True
    )
    program_id = fields.Many2one("g2p.program", "Program", required=True, tracking=True)
    sequence = fields.Integer(required=True, tracking=True, readonly=True, default=1)
    start_date = fields.Date(required=True, tracking=True)
    end_date = fields.Date(required=True, tracking=True)
    state = fields.Selection(
        [(STATE_DRAFT, "Draft"), (STATE_ACTIVE, "Active"), (STATE_ENDED, "Ended")],
        default="draft",
        tracking=True,
    )

    cycle_membership_ids = fields.One2many(
        "g2p.cycle.membership", "cycle_id", "Cycle Memberships"
    )
    voucher_ids = fields.One2many("g2p.voucher", "cycle_id", "Vouchers")

    @api.model
    def get_beneficiaries(self, state):
        domain = [("state", "in", state)]
        for rec in self:
            return rec.cycle_membership_ids.search(domain)

    # TODO: JJ - Add a way to link reports/Dashboard about this cycle.

    # TODO: Implement the method that will call the different managers

    # @api.model
    def copy_beneficiaries_from_program(self):
        # _logger.info("Copying beneficiaries from program, cycles: %s", cycles)
        self.ensure_one()
        self.program_id.get_manager(
            constants.MANAGER_CYCLE
        ).copy_beneficiaries_from_program(self)

    def verify_eligibility(self):
        # 1. Verify the eligibility of the beneficiaries using eligibility_manager.validate_cycle_eligibility()
        pass

    def notify_cycle_started(self):
        # 1. Notify the beneficiaries using notification_manager.cycle_started()
        pass

    def prepare_entitlement(self):
        # 1. Prepare the entitlement of the beneficiaries using entitlement_manager.prepare_vouchers()
        beneficiaries = self.get_beneficiaries(["enrolled"])
        self.program_id.get_manager(constants.MANAGER_ENTITLEMENT).prepare_vouchers(
            self, beneficiaries
        )

    def validate_entitlement(self):
        # 1. Make sure the user has the right to do this
        # 2. Validate the entitlement of the beneficiaries using entitlement_manager.validate_vouchers()
        pass

    def export_distribution_list(self):
        # Not sure if this should be here.
        # It could be customizable reports based on https://github.com/OCA/reporting-engine
        pass

    def duplicate(self, new_start_date):
        # 1. Make sure the user has the right to do this
        # 2. Copy the cycle using the cycle manager
        pass

    def on_start_date_change(self):
        # cycle_manager.on_start_date_change(self, start_date)
        pass

    def open_cycle_form(self):
        return {
            "name": "Cycle",
            "view_mode": "form",
            "res_model": "g2p.cycle",
            "res_id": self.id,
            "view_id": self.env.ref("g2p_programs.view_cycle_form").id,
            "type": "ir.actions.act_window",
            "target": "new",
        }
