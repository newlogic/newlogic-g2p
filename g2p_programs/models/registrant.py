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
from odoo import api, fields, models, _

class G2PRegistrant(models.Model):
    _inherit = 'res.partner'

    #Custom Fields
    program_membership_ids = fields.One2many('g2p.program_membership','partner_id','Program Memberships')
    cycle_ids = fields.One2many('g2p.cycle.membership','partner_id','Cycle Memberships')
    voucher_ids = fields.One2many('g2p.voucher','partner_id','Vouchers')