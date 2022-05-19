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


class G2PGroup(models.Model):
    _inherit = "res.partner"

    kind = fields.Many2one("g2p.group.kind", "Kind", tracking=True)
    group_membership_ids = fields.One2many(
        "g2p.group.membership", "group", "Group Members"
    )
    is_partial_group = fields.Boolean("Partial Group")

    def count_individuals(self, kind=None, criteria=None):
        # Only count active groups
        domain = [('end_date', '=?', False)]

        # TODO: implement the search on the many2Many
        # if kind is not None:
        #     domain += [("kind", "in", state)]

        new_domain = []
        if criteria is not None:
            # This will break if they use logical operators between criteria
            for el in criteria:
                new_domain += [("individual." + el[0], el[1], el[2])]

        total = 0
        for rec in self:
            total += rec.group_membership_ids.search_count(domain)

            return total
