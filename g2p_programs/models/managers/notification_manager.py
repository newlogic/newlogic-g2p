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


class BaseNotification(models.AbstractModel):
    """
    This component is used to notify beneficiaries of their enrollment and other events related to the program
    """

    _name = "g2p.program.notification.manager"

    program_id = fields.Many2one("g2p.program", string="Program", editable=False)
    on_enrolled_in_program = fields.Boolean(
        string="On Enrolled In Program", default=True
    )
    on_cycle_started = fields.Boolean(string="On Cycle Started", default=True)
    on_cycle_ended = fields.Boolean(string="On Cycle Ended", default=True)

    def enrolled_in_program(self, program_memberships):
        return

    def cycle_started(self, program_memberships, cycle):
        return

    def cycle_ended(self, program_memberships, cycle):
        return


class SMSNotification(models.Model):
    _name = "g2p.program.notification.manager.sms"
    _inherit = ["g2p.program.notification.manager", "g2p.job.mixin"]

    on_enrolled_in_program_template = fields.One2many(
        "sms.template", string="On Enrolled In Program Template"
    )
    on_cycle_started_template = fields.One2many(
        "sms.template", string="On Cycle Started Template"
    )
    on_cycle_ended_template = fields.One2many(
        "sms.template", string="On Cycle Ended Template"
    )

    # TODO: render the templates and send the sms using a job
    def enrolled_in_program(self, program_memberships):
        return

    def cycle_started(self, program_memberships, cycle):
        return

    def cycle_ended(self, program_memberships, cycle):
        return
