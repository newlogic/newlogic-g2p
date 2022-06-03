# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class G2PGroup(models.Model):
    _inherit = "res.partner"

    kind = fields.Many2one("g2p.group.kind", "Kind")
    group_membership_ids = fields.One2many(
        "g2p.group.membership", "group", "Group Members"
    )
    is_partial_group = fields.Boolean("Partial Group")

    def count_individuals(self, kinds=None, criteria=None):
        self.ensure_one()
        # Only count active groups

        if self.group_membership_ids:
            domain = [("end_date", "=?", False), ("group", "=", self.id)]
            # To filter the membership by kinds, we first need to find the ID of the kinds we are interested in
            if kinds is not None:
                kind_ids = (
                    self.env["g2p.group.membership.kind"]
                    .search([("name", "in", kinds)])
                    .ids
                )
                domain.extend([("kind", "in", kind_ids)])
            # We can now filter the membership by this domain
            group_membership_ids = self.group_membership_ids.search(domain).ids
        else:
            return 0

        if len(group_membership_ids) == 0:
            return 0

        # Finally filter the res.partner that match the criteria and are related to the group
        domain = [("individual_membership_ids", "in", group_membership_ids)]
        if criteria is not None:
            domain.extend(criteria)
        return self.env["res.partner"].search_count(domain)


class G2PGroupKind(models.Model):
    _name = "g2p.group.kind"
    _description = "Group Kind"
    _order = "id desc"

    name = fields.Char("Kind")
