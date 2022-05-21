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

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class G2PProgram(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin", "g2p.job.mixin"]
    _name = "g2p.program"
    _description = "Program"
    _order = "id desc"
    _check_company_auto = True

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

    def count_beneficiaries(self, state=None):

        domain = []
        if state is not None:
            domain = [("state", "in", state)]

        total = 0
        for rec in self.search([]):
            total += rec.program_membership_ids.search_count(domain)
        return {"value": total}

    # TODO: JJ - Add a way to link reports/Dashboard about this program.

    # TODO: Implement the method that will call the different managers
    def import_beneficiaries(self):
        # 1. get the beneficiaries using the eligibility_manager.import_eligible_registrants()
        for rec in self:
            if rec.eligibility_managers:
                err_ctr = 0
                for el in rec.eligibility_managers:
                    # Add import to queue job.
                    if not el.manager_ref_id.with_delay().import_eligible_registrants():
                        err_ctr += 1
                if err_ctr == 0:
                    # Added import to queue job. Show success notification!
                    title = _("ON QUEUE!")
                    message = _(
                        "The import was put on queue. Re-open this form later to refresh the program members."
                    )
                    kind = "success"  # warning, danger, info, success
                elif err_ctr == len(rec.eligibility_managers):
                    # No registrants imported. Show error message!
                    title = _("ERROR!")
                    message = _("There are no registrants imported.")
                    kind = "danger"
                elif err_ctr < len(rec.eligibility_managers):
                    # Not all registrants are imported. Show warning!
                    title = _("WARNING!")
                    message = _(
                        "%s out of %s managers are not imported."
                        % (err_ctr, len(rec.eligibility_managers))
                    )
                    kind = "warning"

            else:
                # No eligibility managers entered. Show error message!
                title = _("ERROR!")
                message = _("There are no eligibility managers defined.")
                kind = "danger"

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": title,
                    "message": message,
                    "sticky": False,
                    "type": kind,
                },
            }

    def enroll_eligible_registrants(self):
        # TODO: JJ - Think about how can we make it asynchronous.
        for rec in self:
            members = rec.program_membership_ids
            _logger.info("members: %s", members)
            if rec.eligibility_managers:
                for el in rec.eligibility_managers:
                    members = el.manager_ref_id.enroll_eligible_registrants(members)
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
                    message = _(
                        "%s Beneficiaries enrolled."
                        % len(not_enrolled)
                    )
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
            _logger.info("rec.cycle_managers: %s", len(rec.cycle_managers))
            _logger.info("rec.program_managers: %s", rec.program_managers)
            if len(rec.cycle_managers) == 0:
                message = _("No Eligibility Manager defined.")
                kind = "error"
            elif len(rec.program_managers) == 0:
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

            rec.program_managers.ensure_one()
            rec.cycle_managers.ensure_one()
            for pm in rec.program_managers:
                _logger.info("-" * 80)
                _logger.info("pm: %s", pm)
                new_cycle = pm.manager_ref_id.new_cycle()
                message = _(
                    "New cycle %s created." % new_cycle.name
                )
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
