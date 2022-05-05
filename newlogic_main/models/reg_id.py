# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class RegistrantID(models.Model):
    _name = 'nl.reg.id'
    _description = 'Registrant ID'
    _order = 'id desc'

    registrant = fields.Many2one('res.partner','Registrant')
    id_type = fields.Many2one('nl.id.type','ID Type')
    value = fields.Char('Value', size=100)

    #Todo: name_get, name_search