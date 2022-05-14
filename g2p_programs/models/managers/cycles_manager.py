from odoo import api, fields, models


class BaseCyclesManager(models.AbstractModel):

    _name = "g2p.cycles.manager"

    _program = None

    def init_component(self, program):
        self._program = program

    def last_cycle(self):
        """
        Returns the last cycle of the program
        Returns:
            cycle: the last cycle of the program
        """
        raise NotImplementedError()

    def next_cycle(self):
        """
        Create the next cycle of the program
        Returns:
            cycle: the newly created cycle
        """
        raise NotImplementedError()

    def active_cycle(self):
        """
        Returns the active cycle of the program
        Returns:
            cycle: the active cycle of the program
        """
        raise NotImplementedError()

    def activate_cycle(self, cycle):
        """
        Activate the cycle
        Args:
            cycle: the cycle to activate
        """
        raise NotImplementedError()
