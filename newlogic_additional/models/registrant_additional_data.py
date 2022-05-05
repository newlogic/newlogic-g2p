# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class NLRegistrantAdditionalData(models.Model):
    _name = 'nl.registrant.additional.data'
    _description = "Registrant Additional Data"
    _order = 'id desc'

    registrant = fields.Many2one('res.partner', 'Registrant')
    data = fields.Many2one('nl.additional.data', 'Data')
    json_path = fields.Text('JSON Path')