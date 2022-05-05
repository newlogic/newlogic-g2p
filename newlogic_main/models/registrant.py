# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class Registrant(models.Model):
    _inherit = 'res.partner'

    #Custom Fields
    #Todo: location = fields.Many2one('nl.location'), in location module
    #Address (exist in res.partner: Address fields)
    addl_fields = fields.Text('Additional Fields')
    disabled = fields.Datetime('Date Disabled', tracking=True)
    disabled_reason = fields.Text('Reason for disabling')
    disabled_by = fields.Many2one('res.users', 'Disabled by', tracking=True)
    #Tag (exist in res.partner: category_id)
    #Todo: data_source_id = fields.Many2one('nl.data.source')
    
    registrant = fields.Boolean('Registrant')
    is_group = fields.Boolean('Group')

