from odoo import api, fields, models


class BaseEligibility(models.AbstractModel):
    _name = "g2p.program_membership.manager"

    _program = None

    def init_component(self, program):
        self._program = program

    def validate_program_eligibility(self, program_membership):
        """
        This method is used to validate if a user match the criteria needed to be enrolled in a program.
        Args:
            program_membership:

        Returns:
            bool: True if the user match the criterias, False otherwise.
        """
        raise NotImplementedError()

    def validate_cycle_eligibility(self, cycle, program_membership):
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
