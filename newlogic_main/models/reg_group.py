# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class RegGroups(models.Model):
    _name = 'nl.reg.group'
    _description = "Group Registrant"
    _order = 'id desc'

    name = fields.Char('Group Name')
    kind = fields.Selection([('Household','Household'),('Families','Families')],'Kind')