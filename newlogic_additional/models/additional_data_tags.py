# -*- coding: utf-8 -*-
from odoo import fields, models


class G2PAdditionalDataTags(models.Model):
    _name = 'g2p.additional.data.tags'
    _description = "Tags"
    _order = 'id desc'

    
    name = fields.Char(string="Name")