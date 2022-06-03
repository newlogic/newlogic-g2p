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
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class G2PIndividual(models.Model):
    _inherit = "res.partner"

    family_name = fields.Char("Family Name", translate=True)
    given_name = fields.Char("Given Name", translate=True)
    addl_name = fields.Char("Additional Name", translate=True)
    birth_place = fields.Char("Birth Place")
    birthdate_not_exact = fields.Boolean("Birthdate not exact")
    birthdate = fields.Date("Date of Birth")
    age = fields.Char(compute="_compute_calc_age", string="Age", size=50, readonly=True)
    gender = fields.Selection(
        [("Female", "Female"), ("Male", "Male"), ("Other", "Other")],
        "Gender",
    )
    registration_date = fields.Date("Registration Date")
    individual_membership_ids = fields.One2many(
        "g2p.group.membership", "individual", "Membership to Groups"
    )

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

    def _recompute_parent_groups(self, records):
        fields = self._get_calculated_group_fields()
        for line in records:
            if line.is_registrant and not line.is_group:
                groups = line.individual_membership_ids.mapped("group")

                for field in fields:
                    self.env.add_to_compute(field, groups)

    def _get_calculated_group_fields(self):
        model_fields_id = self._fields
        fields = []
        for field_name, field in model_fields_id.items():
            els = field_name.split("_")
            if field.compute and len(els) >= 3 and els[2] == "grp" and els[1] == "crt":
                fields.append(field)
        return fields

    def write(self, vals):
        res = super(G2PIndividual, self).write(vals)
        self._recompute_parent_groups(self)
        return res

    @api.model_create_multi
    @api.returns("self", lambda value: value.id)
    def create(self, vals_list):
        res = super(G2PIndividual, self).create(vals_list)
        self._recompute_parent_groups(res)
        return res
