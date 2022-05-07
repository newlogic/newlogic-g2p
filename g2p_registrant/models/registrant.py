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

class G2PRegistrant(models.Model):
    _inherit = 'res.partner'

    #Custom Fields
    #Todo: location = fields.Many2one('g2p.location'), in location module
    address = fields.Text('Address', tracking=True)
    #addl_fields = fields.Text('Additional Fields', tracking=True)
    disabled = fields.Datetime('Date Disabled', tracking=True)
    disabled_reason = fields.Text('Reason for disabling', tracking=True)
    disabled_by = fields.Many2one('res.users', 'Disabled by', tracking=True)
    #Tag (exist in res.partner: category_id)
    
    is_registrant = fields.Boolean('Registrant')
    is_group = fields.Boolean('Group')

    #def disable_registrant(self):
    #    for rec in self:
    #        if not rec.disabled:
    #            rec.update({
    #                'disabled':fields.Datetime.now(),
    #                'disabled_by':self.env.user,
    #            })

    def enable_registrant(self):
        for rec in self:
            if rec.disabled:
                rec.update({
                    'disabled':None,
                    'disabled_by':None,
                    'disabled_reason':None,
                })