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


class G2PProgram(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin", "g2p.job.mixin"]
    _name = "g2p.program"
    _description = "Program"
    _order = "id desc"
    _check_company_auto = True

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
    # TODO: for `eligibility_manager`, we should allow to have multiple managers and the order of the steps
    #  should be defined by the user
    eligibility_manager = fields.Selection([])
    notification_manager = fields.Selection([])

    # Cycle steps
    cycle_manager = fields.Selection([])
    entitlement_manager = fields.Selection([])

    reconciliation_manager = fields.Selection([])
    reconciliation_manager = fields.Selection([])

    number_of_cycles = fields.Integer(default=1)

    program_membership_ids = fields.One2many(
        "g2p.program_membership", "program_id", "Program Memberships"
    )
    cycle_ids = fields.One2many("g2p.cycle", "program_id", "Cycles")

    # TODO: Implement the method that will call the different managers
    def import_beneficiaries(self):
        # 1. get the beneficiaries using the eligibility_manager.import_eligible_registrants()
        pass

    def verify_eligibility(self):
        # 1. Verify the eligibility of the beneficiaries using eligibility_manager.validate_program_eligibility()
        pass

    def notify_eligible_beneficiaries(self):
        # 1. Notify the beneficiaries using notification_manager.enrolled_in_program()
        pass

    def create_new_cycle(self):
        # 1. Create the next cycle using cycles_manager.new_cycle()
        pass
