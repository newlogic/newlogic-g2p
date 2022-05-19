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
from odoo import api, fields, models


class DeduplicationManager(models.Model):
    _name = "g2p.deduplication.manager"
    _description = "Deduplication Manager"
    _inherit = "g2p.manager.mixin"

    program_id = fields.Many2one("g2p.program", "Program")

    @api.model
    def _selection_manager_ref_id(self):
        selection = super()._selection_manager_ref_id()
        new_managers = [
            ("g2p.deduplication.manager.id_dedup", "ID Deduplication"),
            ("g2p.deduplication.manager.phone_number", "Phone Number Deduplication"),
        ]
        for new_manager in new_managers:
            if new_manager not in selection:
                selection.append(new_manager)
        return selection


class BaseDeduplication(models.AbstractModel):
    _name = "g2p.base.deduplication.manager"
    _description = "Base Deduplication Manager"

    # Kind of deduplication possible
    _capability_individual = False
    _capability_group = False

    name = fields.Char("Manager Name", required=True)
    program_id = fields.Many2one("g2p.program", string="Program", required=True)
    capability_individual = fields.Boolean(
        "Deduplicate Individuals", default=_capability_individual
    )
    capability_group = fields.Boolean("Deduplicate Groups", default=_capability_group)

    def check_duplicates(self, program_membership):
        raise NotImplementedError()


class IDDocumentDeduplication(models.Model):
    """
    When this model is added, it should add also the IDDocumentDeduplicationEligibility to the eligibility
    criteria.
    """

    _name = "g2p.deduplication.manager.id_dedup"
    _inherit = ["g2p.base.deduplication.manager", "g2p.manager.source.mixin"]
    _description = "ID Deduplication Manager"

    supported_id_document_types = fields.Many2many(
        "g2p.id.type", string="Supported ID Document Types"
    )

    def check_duplicates(self, program_memberships):
        # TODO: check if beneficiaries still match the criterias
        return True


class PhoneNumberDeduplication(models.Model):
    """
    When this model is added, it should add also the PhoneNumberDeduplicationEligibility to the eligibility
    criteria.
    """

    _name = "g2p.deduplication.manager.phone_number"
    _inherit = ["g2p.base.deduplication.manager", "g2p.manager.source.mixin"]
    _description = "Phone Number Deduplication Manager"

    # if set, we verify that the phone number match a given regex
    phone_regex = fields.Char(string="Phone Regex")

    def check_duplicates(self, program_memberships):
        # TODO: check if beneficiaries still match the criterias
        return True


class IDPhoneEligibilityManager(models.Model):
    """
    Add the ID Document and Phone Number Deduplication in the Eligibility Manager
    """

    _inherit = "g2p.eligibility.manager"

    @api.model
    def _selection_manager_ref_id(self):
        selection = super()._selection_manager_ref_id()
        new_managers = [
            ("g2p.program_membership.manager.id_dedup", "ID Document Eligibility"),
            ("g2p.program_membership.manager.phone_number", "Phone Number Eligibility"),
        ]
        for new_manager in new_managers:
            if new_manager not in selection:
                selection.append(new_manager)
        return selection


class IDDocumentDeduplicationEligibility(models.Model):
    """
    This model is used to check if a beneficiary has the required documents to be deduplicated.
    It uses the IDDocumentDeduplication configuration to perform the check
    """

    _name = "g2p.program_membership.manager.id_dedup"
    _inherit = ["g2p.program_membership.manager", "g2p.manager.source.mixin"]
    _description = "ID Document Deduplication Eligibility"

    def verify_program_eligibility(self, program_memberships):
        # TODO: check if beneficiaries still match the criterias
        return True

    def verify_cycle_eligibility(self, cycle, program_memberships):
        return self.verify_program_eligibility(program_memberships)


class PhoneNumberDeduplicationEligibility(models.Model):
    """
    This model is used to check if a beneficiary has a phone number to be deduplicated
    It uses the PhoneNumberDeduplication configuration to perform the check
    """

    _name = "g2p.program_membership.manager.phone_number"
    _inherit = ["g2p.program_membership.manager", "g2p.manager.source.mixin"]
    _description = "Phone Number Deduplication Eligibility"

    def verify_program_eligibility(self, program_memberships):
        # TODO: check if beneficiaries still match the criterias
        return True

    def verify_cycle_eligibility(self, cycle, program_memberships):
        return self.verify_program_eligibility(program_memberships)
