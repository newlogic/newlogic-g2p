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

from odoo import _, api, fields, models

from . import constants

_logger = logging.getLogger(__name__)


class G2PCycle(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin", "g2p.job.mixin"]
    _name = "g2p.cycle"
    _description = "Cycle"
    _order = "sequence asc"
    _check_company_auto = True

    STATE_DRAFT = constants.STATE_DRAFT
    STATE_TO_APPROVE = constants.STATE_TO_APPROVE
    STATE_APPROVED = constants.STATE_APPROVED
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
        [
            (STATE_DRAFT, "Draft"),
            (STATE_TO_APPROVE, "To Approve"),
            (STATE_APPROVED, "Approved"),
            (STATE_ACTIVE, "Active"),
            (STATE_ENDED, "Ended"),
        ],
        default="draft",
        tracking=True,
    )

    cycle_membership_ids = fields.One2many(
        "g2p.cycle.membership", "cycle_id", "Cycle Memberships"
    )
    voucher_ids = fields.One2many("g2p.voucher", "cycle_id", "Vouchers")

    # Statistics
    members_count = fields.Integer(
        string="# Beneficiaries", compute="_compute_members_count"
    )
    vouchers_count = fields.Integer(
        string="# Vouchers", compute="_compute_vouchers_count"
    )

    @api.depends("cycle_membership_ids")
    def _compute_members_count(self):
        for rec in self:
            members_count = 0
            if rec.cycle_membership_ids:
                members_count = len(
                    rec.cycle_membership_ids.filtered(lambda mb: mb.state == "enrolled")
                )
            rec.update({"members_count": members_count})

    @api.depends("voucher_ids")
    def _compute_vouchers_count(self):
        for rec in self:
            vouchers_count = 0
            if rec.voucher_ids:
                vouchers_count = len(
                    rec.voucher_ids.filtered(lambda mb: mb.state == "approved")
                )
            rec.update({"vouchers_count": vouchers_count})

    def approve(self):
        # 1. Make sure the user has the right to do this
        # 2. Approve the cycle using the cycle manager
        pass

    @api.model
    def get_beneficiaries(self, state):
        if isinstance(state, str):
            state = [state]
        for rec in self:
            domain = [("state", "in", state), ("cycle_id", "=", rec.id)]
            return self.env["g2p.cycle.membership"].search(domain)

    # TODO: JJ - Add a way to link reports/Dashboard about this cycle.

    # TODO: Implement the method that will call the different managers

    # @api.model
    def copy_beneficiaries_from_program(self):
        # _logger.info("Copying beneficiaries from program, cycles: %s", cycles)
        self.ensure_one()
        self.program_id.get_manager(
            constants.MANAGER_CYCLE
        ).copy_beneficiaries_from_program(self)

    def check_eligibility(self, beneficiaries=None):
        self.program_id.get_manager(constants.MANAGER_CYCLE).check_eligibility(
            self, beneficiaries
        )

    def notify_cycle_started(self):
        # 1. Notify the beneficiaries using notification_manager.cycle_started()
        pass

    def prepare_entitlement(self):
        # 1. Prepare the entitlement of the beneficiaries using entitlement_manager.prepare_vouchers()
        self.program_id.get_manager(constants.MANAGER_CYCLE).prepare_vouchers(self)

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

    @api.onchange("start_date")
    def on_start_date_change(self):
        self.program_id.get_manager(constants.MANAGER_CYCLE).on_start_date_change(self)

    @api.onchange("state")
    def on_state_change(self):
        self.program_id.get_manager(constants.MANAGER_CYCLE).on_state_change(self)

    def open_members_form(self):
        self.ensure_one()

        action = {
            "name": _("Cycle Members"),
            "type": "ir.actions.act_window",
            "res_model": "g2p.cycle.membership",
            "context": {"create": False, "default_cycle_id": self.id},
            "view_mode": "list,form",
            "domain": [("cycle_id", "=", self.id), ("state", "=", "enrolled")],
        }
        return action

    def open_vouchers_form(self):
        self.ensure_one()

        action = {
            "name": _("Cycle Vouchers"),
            "type": "ir.actions.act_window",
            "res_model": "g2p.voucher",
            "context": {"create": False, "default_cycle_id": self.id},
            "view_mode": "list,form",
            "domain": [("cycle_id", "=", self.id), ("state", "=", "approved")],
        }
        return action
