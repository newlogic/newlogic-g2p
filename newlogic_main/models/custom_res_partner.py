# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class Registrants(models.Model):
    _inherit = 'res.partner'

    #Custom Fields
    date_disabled = fields.Datetime('Date Disabled', tracking=True)
    reason_disabled = fields.Text('Reason for disabling')
    userid_disabled = fields.Many2one('res.users', 'Disabled by', tracking=True)
    individual_id = fields.Many2one('nl.reg.individual','Individual')
    is_group = fields.Boolean('Group')
    group_id = fields.Many2one('nl.reg.group','Group')

    registrant = fields.Boolean('Registrant')

    @api.onchange('registrant','individual_id.family_name','individual_id.given_name','individual_id.addl_name')
    def partner_name_change(self):
        vals = {}
        if self.registrant and self.individual_id:
            name = ''
            if self.individual_id.family_name:
                name += self.individual_id.family_name + ', '
            if self.individual_id.given_name:
                name += self.individual_id.given_name + ' '
            if self.individual_id.addl_name:
                name += self.individual_id.addl_name + ' '

            vals.update({'name': name.upper()})
            self.update(vals)