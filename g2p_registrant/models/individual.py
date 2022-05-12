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
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class G2PIndividual(models.Model):
    _inherit = "res.partner"

    family_name = fields.Char("Family Name", translate=True, tracking=True)
    given_name = fields.Char("Given Name", translate=True, tracking=True)
    addl_name = fields.Char("Additional Name", translate=True, tracking=True)
    birth_place = fields.Char("Birth Place", tracking=True)
    birthdate_exact = fields.Boolean("Birthdate Exact")
    birthdate = fields.Date("Date of Birth", tracking=True)
    age = fields.Char(compute="_compute_calc_age", string="Age", size=50, readonly=True)
    gender = fields.Selection(
        [("Female", "Female"), ("Male", "Male"), ("Other", "Other")],
        "Gender",
        tracking=True,
    )
    registration_date = fields.Date("Registration Date", tracking=True)
    individual_membership_ids = fields.One2many("g2p.group.membership", "individual", "Membership to Groups")

    @api.onchange("is_group", "family_name", "given_name", "addl_name")
    def name_change(self):
        vals = {}
        if not self.is_group:
            name = ""
            if self.family_name:
                name += self.family_name + ", "
            if self.given_name:
                name += self.given_name + " "
            if self.addl_name:
                name += self.addl_name + " "
            vals.update({"name": name.upper()})
            self.update(vals)

    @api.depends("birthdate")
    def _compute_calc_age(self):
        for line in self:
            line.age = self.compute_age_from_dates(line.birthdate)

    def compute_age_from_dates(self, partner_dob):
        now = datetime.strptime(str(fields.Datetime.now())[:10], "%Y-%m-%d")
        if partner_dob:
            dob = partner_dob
            delta = relativedelta(now, dob)
            # years_months_days = str(delta.years) +"y "+ str(delta.months) +"m "+ str(delta.days)+"d"
            years_months_days = str(delta.years)
        else:
            years_months_days = "No Birthdate!"
        return years_months_days
