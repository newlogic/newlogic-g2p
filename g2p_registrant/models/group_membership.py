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

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class G2PGroupMembership(models.Model):
    _name = "g2p.group.membership"
    _description = "Group Membership"
    _order = "id desc"
    _inherit = ["mail.thread"]

    group = fields.Many2one(
        "res.partner",
        "Group",
        required=True,
        domain=[("is_group", "=", True), ("is_registrant", "=", True)],
        tracking=True,
    )
    individual = fields.Many2one(
        "res.partner",
        "Individual",
        required=True,
        domain=[("is_group", "=", False), ("is_registrant", "=", True)],
        tracking=True,
    )
    kind = fields.Many2many("g2p.group.membership.kind", string="Kind", tracking=True)
    start_date = fields.Datetime(
        "Start Date", tracking=True, default=lambda self: fields.Datetime.now()
    )
    end_date = fields.Datetime(
        "End Date", tracking=True
    )  # TODO: Should rename `ended_date` add a check that the date is in the past

    @api.onchange("kind")
    def _kind_onchange(self):
        head_count = 0
        principal_count = 0
        for line in self.group.group_membership_ids:
            for rec_line in line.kind:
                kind_id = str(rec_line.id)
                kind_str = ""
                for m in kind_id:
                    if m.isdigit():
                        kind_str = kind_str + m
                _logger.info("Kind ID: %s" % kind_str)
                if rec_line.id == 1 or kind_str == "1":
                    head_count += 1
                if rec_line.id == 2 or kind_str == "2":
                    principal_count += 1
        if head_count > 1 and principal_count > 1:
            raise ValidationError(_("Only one head or principal is allowed per group"))
        elif head_count > 1:
            raise ValidationError(_("Only one head is allowed per group"))
        elif principal_count > 1:
            raise ValidationError(_("Only one principal is allowed per group"))

    @api.constrains("individual")
    def _check_group_members(self):
        rec_count = 0
        for rec in self.group.group_membership_ids:
            if self.individual.id == rec.individual.id:
                rec_count += 1
        if rec_count > 1:
            raise ValidationError(_("Duplication of Member is not allowed "))

    def name_get(self):
        res = super(G2PGroupMembership, self).name_get()
        for rec in self:
            name = "NONE"
            if rec.group:
                name = rec.group.name
            res.append((rec.id, name))
        return res

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        if name:
            args = [("group", operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def open_individual_form(self):
        return {
            "name": "Individual Member",
            "view_mode": "form",
            "res_model": "res.partner",
            "res_id": self.individual.id,
            "view_id": self.env.ref("g2p_registrant.view_individuals_form").id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_is_group": False},
            "flags": {"mode": "readonly"},
        }

    def open_group_form(self):
        return {
            "name": "Group Membership",
            "view_mode": "form",
            "res_model": "res.partner",
            "res_id": self.group.id,
            "view_id": self.env.ref("g2p_registrant.view_groups_form").id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_is_group": True},
            "flags": {"mode": "readonly"},
        }


class G2PGroupMembershipKind(models.Model):
    _name = "g2p.group.membership.kind"
    _description = "Group Membership Kind"
    _order = "id desc"

    name = fields.Char("Kind")
