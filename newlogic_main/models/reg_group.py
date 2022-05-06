# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class G2PRegGroup(models.Model):
    _inherit = 'res.partner'

    #name (exist in res.partner: name)
    kind = fields.Selection([('Household','Household'),('Families','Families')],'Kind', tracking=True)
    group_membership_ids = fields.One2many('g2p.group.membership','group','Group Members')

    #partner_ids = fields.Many2many('res.partner', column1='category_id', column2='partner_id', string='Partners')