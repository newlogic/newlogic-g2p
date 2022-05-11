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
from odoo import _, api, fields, models

class G2PCycle(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "g2p.cycle"
    _description = "Cycle"
    _order = 'id desc'
    _check_company_auto = True

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, tracking=True)
    program_id = fields.Many2one('g2p.program', 'Program', required=True, tracking=True)
    
    cycle_membership_ids = fields.One2many('g2p.cycle.membership','cycle_id','Cycle Memberships')
    voucher_ids = fields.One2many('g2p.voucher','cycle_id','Vouchers')