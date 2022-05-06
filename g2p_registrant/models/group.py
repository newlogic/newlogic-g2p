# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _

from odoo.exceptions import AccessError, UserError, ValidationError, Warning

class G2PGroup(models.Model):
    _inherit = 'res.partner'

    #name (exist in res.partner: name)
    kind = fields.Selection([('Household','Household'),('Families','Families')],'Kind', tracking=True)
    group_membership_ids = fields.One2many('g2p.group.membership','group','Group Members')

    #partner_ids = fields.Many2many('res.partner', column1='category_id', column2='partner_id', string='Partners')