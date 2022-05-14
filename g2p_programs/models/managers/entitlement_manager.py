from odoo import api, fields, models


class BaseEntitlementManager(models.AbstractModel):
    _name = "g2p.program.entitlement.manager"

    _program = None

    def init_component(self, program):
        self._program = program

    def prepare_entitlements(self, cycle, cycle_memberships):
        """
        This method is used to prepare the entitlement list of the beneficiaries.
        :param cycle: The cycle.
        :param cycle_memberships: The beneficiaries.
        :return:
        """
        raise NotImplementedError()

    def validate_entitlements(self, cycle, cycle_memberships):
        """
        This method is used to validate the entitlement list of the beneficiaries.
        :param cycle: The cycle.
        :param cycle_memberships: The beneficiaries.
        :return:
        """
        raise NotImplementedError()
