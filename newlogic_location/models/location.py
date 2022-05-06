# -*- coding: utf-8 -*-
#from datetime import datetime, timedelta
#from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class Location(models.Model):
    _name = 'nl.location'
    _description = 'Location'
    _order = 'id desc'

    name = fields.Char('Name')
    code = fields.Char('Code')
    altnames = fields.Char('Alternate Name')
    level = fields.Integer('Level')

