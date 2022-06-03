# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
import collections
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class DeduplicationManager(models.Model):
    _name = "g2p.deduplication.manager"
    _description = "Deduplication Manager"
    _inherit = "g2p.manager.mixin"

    program_id = fields.Many2one("g2p.program", "Program")

    @api.model
    def _selection_manager_ref_id(self):
        selection = super()._selection_manager_ref_id()
        new_managers = [
            ("g2p.deduplication.manager.default", "Default Deduplication"),
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

    def deduplicate_beneficiaries(self, states):
        raise NotImplementedError()


class DefaultDeduplication(models.Model):
    _name = "g2p.deduplication.manager.default"
    _inherit = ["g2p.base.deduplication.manager", "g2p.manager.source.mixin"]
    _description = "Default Deduplication Manager"

    _capability_individual = True
    _capability_group = True

    def deduplicate_beneficiaries(self, states):
        for rec in self:
            duplicate_beneficiaries = []
            program = rec.program_id
            beneficiaries = program.get_beneficiaries(states)
            # duplicates
            _logger.info("Deduplicate beneficiaries: %s", beneficiaries)
            if program.target_type == "group":
                duplicate_beneficiaries = self._check_duplicate_by_individual_ids(
                    beneficiaries
                )
            return len(duplicate_beneficiaries)

    def _record_duplicate(self, manager, beneficiary_ids, reason):
        """
        This method is used to record a duplicate beneficiary.
        :param beneficiary: The beneficiary.
        :param reason: The reason.
        :param comment: The comment.
        :return:
        """

        # TODO: check this group does not exist already with the same manager and the same beneficiaries or
        #  a subset of them.
        #  1. If the state has been changed to no_duplicate, then we should not record it as duplicate unless there are
        #  additional beneficiaries in the group.
        #  2. Otherwise we update the record.

        _logger.info("Record duplicate: %s", beneficiary_ids)
        data = {
            "beneficiary_ids": [(6, 0, beneficiary_ids)],
            "state": "duplicate",
            "reason": reason,
            "deduplication_manager_id": manager,
        }
        _logger.info("Record duplicate: %s", data)

        self.env["g2p.program.membership.duplicate"].create(data)

    def _check_duplicate_by_individual_ids(self, beneficiaries):
        """
        This method is used to check if there are any duplicates among the individuals.
        :param beneficiary_ids: The beneficiaries.
        :return:
        """
        _logger.info("-" * 100)
        group_ids = beneficiaries.mapped("partner_id.id")
        group_memberships = self.env["g2p.group.membership"].search(
            [("group", "in", group_ids)]
        )
        _logger.info("group_memberships: %s", group_memberships)

        individuals_ids = [rec.individual.id for rec in group_memberships]
        _logger.info("individuals_ids: %s", individuals_ids)

        duplicate_individuals = [
            item
            for item, count in collections.Counter(individuals_ids).items()
            if count > 1
        ]
        _logger.info("Duplicate individuals: %s", duplicate_individuals)

        group_with_duplicates = self.env["g2p.group.membership"].search(
            [("group", "in", group_ids), ("individual", "in", duplicate_individuals)]
        )

        _logger.info("group_with_duplicates: %s", group_with_duplicates)
        group_of_duplicates = {}
        for group_membership in group_with_duplicates:
            _logger.info(
                "group_membership.individual.id: %s -> %s"
                % (group_membership.individual.id, group_membership.group.id)
            )
            if group_membership.individual.id not in group_of_duplicates:
                group_of_duplicates[group_membership.individual.id] = []
            group_of_duplicates[group_membership.individual.id].append(
                group_membership.group.id
            )

        _logger.info("group_of_duplicates: %s", group_of_duplicates)
        for _individual, group_ids in group_of_duplicates.items():

            duplicate_beneficiaries = beneficiaries.filtered(
                lambda rec: rec.partner_id.id in group_ids
            )
            duplicate_beneficiariy_ids = duplicate_beneficiaries.mapped("id")

            self._record_duplicate(
                self, duplicate_beneficiariy_ids, "Duplicate individuals"
            )

            duplicated_enrolled = duplicate_beneficiaries.filtered(
                lambda rec: rec.state == "enrolled"
            )
            if len(duplicated_enrolled) == 1:
                # If there is only 1 enrolled that is duplicated, the enrolled one should not be marked as duplicate.
                # otherwise if there is more than 1, then there is a problem!
                # TODO: check how to handle this
                duplicated_enrolled.write({"state": "enrolled"})
                duplicate_beneficiaries = duplicate_beneficiaries.filtered(
                    lambda rec: rec.state != "enrolled"
                )
            duplicate_beneficiaries.filtered(
                lambda rec: rec.state not in ["exited", "not_eligible", "duplicated"]
            ).write({"state": "duplicated"})

        return group_with_duplicates


class IDDocumentDeduplication(models.Model):
    _name = "g2p.deduplication.manager.id_dedup"
    _inherit = ["g2p.base.deduplication.manager", "g2p.manager.source.mixin"]
    _description = "ID Deduplication Manager"

    supported_id_document_types = fields.Many2many(
        "g2p.id.type", string="Supported ID Document Types"
    )

    def deduplicate_beneficiaries(self, states):
        pass


class PhoneNumberDeduplication(models.Model):
    """
    When this model is added, it should add also the PhoneNumberDeduplicationEligibility to the eligibility
    criteria.
    """

    _name = "g2p.deduplication.manager.phone_number"
    _inherit = ["g2p.base.deduplication.manager", "g2p.manager.source.mixin"]
    _description = "Phone Number Deduplication Manager"

    # # if set, we verify that the phone number match a given regex
    # phone_regex = fields.Char(string="Phone Regex")

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

    def enroll_eligible_registrants(self, program_memberships):
        # TODO: check if beneficiaries still match the criterias
        return True

    def verify_cycle_eligibility(self, cycle, program_memberships):
        return self.enroll_eligible_registrants(program_memberships)


class PhoneNumberDeduplicationEligibility(models.Model):
    """
    This model is used to check if a beneficiary has a phone number to be deduplicated
    It uses the PhoneNumberDeduplication configuration to perform the check
    """

    _name = "g2p.program_membership.manager.phone_number"
    _inherit = ["g2p.program_membership.manager", "g2p.manager.source.mixin"]
    _description = "Phone Number Deduplication Eligibility"

    def enroll_eligible_registrants(self, program_memberships):
        # TODO: check if beneficiaries still match the criterias
        return True

    def verify_cycle_eligibility(self, cycle, program_memberships):
        return self.enroll_eligible_registrants(program_memberships)
