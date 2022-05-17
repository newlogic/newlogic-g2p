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


class BaseEligibility(models.AbstractModel):
    _name = "g2p.program_membership.manager"
    _inherit = "base.programs.manager"
    _description = "Base Eligibility"

    name = fields.Char('Manager Name', required=True)
    program_id = fields.Many2one("g2p.program", string="Program", required=True)

    def verify_program_eligibility(self, program_memberships):
        """
        This method is used to validate if a user match the criteria needed to be enrolled in a program.
        Args:
            program_membership:

        Returns:
            bool: True if the user match the criterias, False otherwise.
        """
        raise NotImplementedError()

    def verify_cycle_eligibility(self, cycle, program_memberships):
        """
        This method is used to validate if a beneficiary match the criteria needed to be enrolled in a cycle.
        Args:
            cycle:
            program_membership:

        Returns:
            bool: True if the cycle match the criterias, False otherwise.
        """
        raise NotImplementedError()

    def import_eligible_registrants(self):
        """
        This method is used to import the beneficiaries in a program.
        Returns:
        """
        raise NotImplementedError()


class SimpleEligibility(models.Model):
    _name = "g2p.program_membership.manager.simple"
    _inherit = "g2p.program_membership.manager"
    _description = "Simple Eligibility"

    support_individual = fields.Boolean(string="Support Individual", default=False)
    support_group = fields.Boolean(string="Support Group", default=False)

    # TODO: cache the parsed domain
    eligibility_domain = fields.Text(string="Domain", default="[]")

    def verify_program_eligibility(self, program_membership):
        # TODO: check if the beneficiary still match the criterias
        return True

    def verify_cycle_eligibility(self, cycle, program_membership):
        return self.verify_program_eligibility(cycle)

    def import_eligible_registrants(self):
        domain = [("is_registrant", "=", True)]
        for rec in self:
            if rec.support_individual and not rec.support_group:
                domain += [('is_group','=',False)]
            if not rec.support_individual and rec.support_group:
                domain += [('is_group','=',True)]
               
            if rec.eligibility_domain:
                domain = domain + rec._safe_eval(self.eligibility_domain)
            results = self.env["res.partner"].search(domain)

            #Add all the matching registrants that are not yet enrolled to the program
            if results:
                registrants = []
                for r in results:
                    registrants.append([0,0,{
                        'partner_id':r.id,
                        'enrollment_date': fields.Date.today(),
                    }])
                rec.program_id.program_membership_ids.with_delay().update({'program_membership_ids':registrants})
                return True
            else:
                return False