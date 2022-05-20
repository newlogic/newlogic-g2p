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

from odoo import fields, models

_logger = logging.getLogger(__name__)


class G2PGroup(models.Model):
    _inherit = "res.partner"

    kind = fields.Many2one("g2p.group.kind", "Kind", tracking=True)
    group_membership_ids = fields.One2many(
        "g2p.group.membership", "group", "Group Members"
    )
    is_partial_group = fields.Boolean("Partial Group")

    def count_individuals(self, kinds=None, criteria=None):
        self.ensure_one()
        for rec in self:
            # Only count active groups
            domain = [("end_date", "=?", False)]
            if rec.group_membership_ids:
                # To filter the membership by kinds, we first need to find the ID of the kinds we are interested in
                if kinds is not None:
                    kind_ids = (
                        self.env["g2p.group.membership.kind"]
                        .search([("name", "in", kinds)])
                        .ids
                    )
                    domain.extend([("kind", "in", kind_ids)])

                # We can now filter the membership by this domain
                group_membership_ids = rec.group_membership_ids.search(domain).ids
            else:
                return 0

            if len(group_membership_ids) == 0:
                return 0

            # Finally filter the res.partner that match the criteria and are related to the group
            domain = [("individual_membership_ids", "in", group_membership_ids)]
            domain.extend(criteria)
            return self.env["res.partner"].search_count(domain)


class G2PGroupKind(models.Model):
    _name = "g2p.group.kind"
    _description = "Group Kind"
    _order = "id desc"

    name = fields.Char("Kind")
