# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class G2PRegistrant(models.Model):
    _inherit = 'res.partner'

    #Custom Fields
    #Todo: location = fields.Many2one('g2p.location'), in location module
    address = fields.Text('Address')
    addl_fields = fields.Text('Additional Fields')
    disabled = fields.Datetime('Date Disabled', tracking=True)
    disabled_reason = fields.Text('Reason for disabling')
    disabled_by = fields.Many2one('res.users', 'Disabled by', tracking=True)
    #Tag (exist in res.partner: category_id)
    
    registrant = fields.Boolean('Registrant')
    is_group = fields.Boolean('Group')

    def disable_registrant(self):
        for rec in self:
            if not rec.disabled:
                rec.update({
                    'disabled':fields.Datetime.now(),
                    'disabled_by':self.env.user,
                })

    def enable_registrant(self):
        for rec in self:
            if rec.disabled:
                rec.update({
                    'disabled':None,
                    'disabled_by':None,
                    'disabled_reason':None,
                })