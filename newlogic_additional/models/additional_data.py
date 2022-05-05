# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class NLAdditionalData(models.Model):
    _name = 'nl.additional.data'
    _description = "Basic Additional Data Object"
    _order = 'id desc'

    
    source = fields.Many2one('nl.datasource', 'Source')
    name = fields.Char(string="Name")
    json = fields.Text('JSON')
    tag = fields.Many2many('nl.additional.data.tags', string='Tag')