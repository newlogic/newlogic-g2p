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


class G2PProgram(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin", "g2p.job.mixin"]
    _name = "g2p.program"
    _description = "Program"
    _order = "id desc"
    _check_company_auto = True

    MANAGER_ELIGIBILITY = constants.MANAGER_ELIGIBILITY
    MANAGER_CYCLE = constants.MANAGER_CYCLE
    MANAGER_PROGRAM = constants.MANAGER_PROGRAM
    MANAGER_ENTITLEMENT = constants.MANAGER_ENTITLEMENT
    MANAGER_DEDUPLICATION = constants.MANAGER_DEDUPLICATION
    MANAGER_NOTIFICATION = constants.MANAGER_NOTIFICATION

    # TODO: Associate a Wallet to each program using the accounting module
    # TODO: (For later) Associate a Warehouse to each program using the stock module for in-kind programs

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, tracking=True
    )
    target_type = fields.Selection(
        selection=[("group", "Group"), ("individual", "Individual")], default="group"
    )

    # delivery_mechanism = fields.Selection([("mobile", "Mobile"), ("bank_account", "Bank Account"),
    # ("id", "ID Document"), ("biometric", "Biometrics")], default='id')

    # Pre-cycle steps
    # TODO: for those, we should allow to have multiple managers and
    #  the order of the steps should be defined by the user
    eligibility_managers = fields.Many2many(
        "g2p.eligibility.manager", string="Eligibility Managers"
    )  # All will be run
    deduplication_managers = fields.Many2many(
        "g2p.deduplication.manager", string="Deduplication Managers"
    )  # All will be run
    # for each beneficiary, their preferred will be used or the first one that works.
    notification_managers = fields.Many2many(
        "g2p.program.notification.manager", string="Notification Managers"
    )
    program_managers = fields.Many2many(
        "g2p.program.manager", string="Program Managers"
    )
    # Cycle steps
    cycle_managers = fields.Many2many("g2p.cycle.manager", string="Cycle Managers")
    entitlement_managers = fields.Many2many(
        "g2p.program.entitlement.manager", string="Entitlement Managers"
    )

    reconciliation_managers = fields.Selection([])

    program_membership_ids = fields.One2many(
        "g2p.program_membership", "program_id", "Program Memberships"
    )
    cycle_ids = fields.One2many("g2p.cycle", "program_id", "Cycles")

    # Statistics
    eligible_beneficiaries_count = fields.Integer(
        string="# Eligible Beneficiaries", compute="_compute_eligible_beneficiaries"
    )

    cycles_count = fields.Integer(string="# Cycles", compute="_compute_cycles")

    @api.depends("program_membership_ids")
    def _compute_eligible_beneficiaries(self):
        for rec in self:
            eligible_beneficiaries_count = 0
            if rec.program_membership_ids:
                eligible_beneficiaries_count = len(
                    rec.program_membership_ids.filtered(
                        lambda bn: bn.state == "enrolled"
                    )
                )
            rec.update({"eligible_beneficiaries_count": eligible_beneficiaries_count})

    @api.depends("cycle_ids")
    def _compute_cycles(self):
        for rec in self:
            cycles_count = 0
            if rec.cycle_ids:
                cycles_count = len(
                    rec.cycle_ids.filtered(lambda bn: bn.state == "approved")
                )
            rec.update({"cycles_count": cycles_count})

    @api.model
    def get_manager(self, kind):
        self.ensure_one()
        for rec in self:
            if kind == self.MANAGER_CYCLE:
                managers = rec.cycle_managers
            elif kind == self.MANAGER_PROGRAM:
                managers = rec.program_managers
            elif kind == self.MANAGER_ENTITLEMENT:
                managers = rec.entitlement_managers
            else:
                raise NotImplementedError("Manager not supported")
            managers.ensure_one()
            for el in managers:
                return el.manager_ref_id

    @api.model
    def get_managers(self, kind):
        self.ensure_one()
        for rec in self:
            if kind == self.MANAGER_ELIGIBILITY:
                managers = rec.eligibility_managers
            elif kind == self.MANAGER_DEDUPLICATION:
                managers = rec.deduplication_managers
            elif kind == self.MANAGER_NOTIFICATION:
                managers = rec.notification_managers
            else:
                raise NotImplementedError("Manager not supported")
            return [el.manager_ref_id for el in managers]

    @api.model
    def get_beneficiaries(self, state):
        if isinstance(state, str):
            state = [state]
        for rec in self:
            domain = [("state", "in", state), ("program_id", "=", rec.id)]
            return self.env["g2p.program_membership"].search(domain)

    # TODO: JJ - Review
    def count_beneficiaries(self, state=None):

        domain = []
        if state is not None:
            domain = [("state", "in", state)]

        return {"value": self.env["g2p.program_membership"].search_count(domain)}

    # TODO: JJ - Add a way to link reports/Dashboard about this program.

    def enroll_eligible_registrants(self):
        # TODO: JJ - Think about how can we make it asynchronous.
        for rec in self:
            members = rec.program_membership_ids
            _logger.info("members: %s", members)
            eligibility_managers = self.get_managers(self.MANAGER_ELIGIBILITY)
            if len(eligibility_managers):
                for el in eligibility_managers:
                    members = el.enroll_eligible_registrants(members)
                # list the one not already enrolled:
                _logger.info("members filtered: %s", members)
                not_enrolled = members.filtered(lambda m: m.state != "enrolled")
                _logger.info("not_enrolled: %s", not_enrolled)
                not_enrolled.write(
                    {
                        "state": "enrolled",
                        "enrollment_date": fields.Datetime.now(),
                    }
                )
                if len(not_enrolled) > 0:
                    message = _("%s Beneficiaries enrolled." % len(not_enrolled))
                    kind = "success"
                else:
                    message = _("No Beneficiaries enrolled.")
                    kind = "warning"
            else:
                message = _("No Eligibility Manager defined.")
                kind = "error"

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Enrollment"),
                    "message": message,
                    "sticky": True,
                    "type": kind,
                },
            }

    def deduplicate_beneficiaries(self):
        # 1. Deduplicate the beneficiaries using deduplication_manager.check_duplicates()
        pass

    def notify_eligible_beneficiaries(self):
        # 1. Notify the beneficiaries using notification_manager.enrolled_in_program()
        pass

    def create_new_cycle(self):
        # 1. Create the next cycle using cycles_manager.new_cycle()
        # 2. Import the beneficiaries from the previous cycle to this one. If it is the first one, import from the
        # program memberships.
        for rec in self:
            message = None
            kind = "success"
            cycle_manager = rec.get_manager(self.MANAGER_CYCLE)
            program_manager = rec.get_manager(self.MANAGER_PROGRAM)
            if cycle_manager is None:
                message = _("No Eligibility Manager defined.")
                kind = "error"
            elif program_manager is None:
                message = _("No Program Manager defined.")
                kind = "error"

            if message is not None:
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": _("Cycle"),
                        "message": message,
                        "sticky": True,
                        "type": kind,
                    },
                }

            _logger.info("-" * 80)
            _logger.info("pm: %s", program_manager)
            new_cycle = program_manager.new_cycle()
            message = _("New cycle %s created." % new_cycle.name)
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Cycle"),
                    "message": message,
                    "sticky": True,
                    "type": kind,
                },
            }

    def open_eligible_beneficiaries_form(self):
        self.ensure_one()

        action = {
            "name": _("Eligible Beneficiaries"),
            "type": "ir.actions.act_window",
            "res_model": "g2p.program_membership",
            "context": {"create": False, "default_program_id": self.id},
            "view_mode": "list,form",
            "domain": [("program_id", "=", self.id), ("state", "=", "enrolled")],
        }
        return action

    def open_cycles_form(self):
        self.ensure_one()

        action = {
            "name": _("Cycles"),
            "type": "ir.actions.act_window",
            "res_model": "g2p.cycle",
            "context": {"create": False, "default_program_id": self.id},
            "view_mode": "list,form",
            "domain": [("program_id", "=", self.id), ("state", "=", "approved")],
        }
        return action
