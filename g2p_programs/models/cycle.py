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


class G2PCycle(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin", "g2p.job.mixin"]
    _name = "g2p.cycle"
    _description = "Cycle"
    _order = "id desc"
    _check_company_auto = True

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, tracking=True
    )
    program_id = fields.Many2one("g2p.program", "Program", required=True, tracking=True)
    sequence = fields.Integer(required=True, tracking=True, editable=False)
    start_date = fields.Date(required=True, tracking=True)
    end_date = fields.Date(required=True, tracking=True)
    status = fields.Selection(
        [("draft", "Draft"), ("active", "Active"), ("ended", "Ended")],
        default="draft",
        tracking=True,
    )

    cycle_membership_ids = fields.One2many(
        "g2p.cycle.membership", "cycle_id", "Cycle Memberships"
    )
    voucher_ids = fields.One2many("g2p.voucher", "cycle_id", "Vouchers")

    # TODO: Implement the method that will call the different managers

    def verify_eligibility(self):
        # 1. Verify the eligibility of the beneficiaries using eligibility_manager.validate_cycle_eligibility()
        pass

    def notify_cycle_started(self):
        # 1. Notify the beneficiaries using notification_manager.cycle_started()
        pass

    def prepare_entitlement(self):
        # 1. Prepare the entitlement of the beneficiaries using entitlement_manager.prepare_vouchers()
        pass

    def validate_entitlement(self):
        # 1. Make sure the user has the right to do this
        # 2. Validate the entitlement of the beneficiaries using entitlement_manager.validate_vouchers()
        pass

    def export_distribution_list(self):
        # Not sure if this should be here.
        pass
