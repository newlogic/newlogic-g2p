from odoo import api, fields, models


class BaseCycleManager(models.AbstractModel):

    _name = "g2p.cycle.manager"

    _program = None
    _cycle = None

    def init_component(self, program, cycle):
        self._program = program
        self._cycle = cycle

    def next_cycle(self):
        """
        Return the next cycle of the program if any
        Returns:
            cycle: the next cycle of the program
        """
        raise NotImplementedError()

    def previous_cycle(self):
        """
        Return the previous cycle of the program if any
        Returns:
            cycle: the previous cycle of the program
        """
        raise NotImplementedError()

    def check_eligibility(self):
        """
        Validate the eligibility of each beneficiaries for the cycle
        """
        raise NotImplementedError()

    def prepare_entitlements(self):
        """
        Prepare the entitlements for the cycle
        """
        raise NotImplementedError()

    def validate_entitlements(self, cycle_memberships):
        """
        Validate the entitlements for the cycle
        """
        raise NotImplementedError()


