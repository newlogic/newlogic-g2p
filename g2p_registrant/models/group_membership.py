# -*- coding: utf-8 -*-
#################################################################################
#   Copyright 2022 Newlogic
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#################################################################################
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _

from odoo.exceptions import AccessError, UserError, ValidationError, Warning

class G2PGroupMembership(models.Model):
    _name = 'g2p.group.membership'
    _description = 'Group Membership'
    _order = 'id desc'

    group = fields.Many2one('res.partner','Group')
    individual = fields.Many2one('res.partner','Individual')
    kind = fields.Many2many('g2p.group.kind',string='Kind')
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')

    def name_get(self):
        res = super(G2PGroupMembership, self).name_get()
        for rec in self:
            name = 'NONE'
            if rec.group:
                name = rec.group.name
            res.append((rec.id, name))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args = [('group', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

class G2PGoupKind(models.Model):
    _name = 'g2p.group.kind'
    _description = 'Group Kind'
    _order = 'id desc'

    name = fields.Char('Kind')