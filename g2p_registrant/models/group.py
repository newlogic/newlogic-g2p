# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _

from odoo.exceptions import AccessError, UserError, ValidationError, Warning

class G2PGroup(models.Model):
    _inherit = 'res.partner'

    kind = fields.Many2one('g2p.group.kind','Kind', tracking=True)
    #kind = fields.Selection([],'Kind')
    group_membership_ids = fields.One2many('g2p.group.membership','group','Group Members')

