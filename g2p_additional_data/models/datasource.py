# -*- coding: utf-8 -*-
from odoo import fields, models

class G2PDataSource(models.Model):
    _name = 'g2p.datasource'
    _description = "Data Source"
    _order = 'id desc'

    parent_id = fields.Many2one('g2p.datasource', 'Parent')
    name = fields.Char(string="Name", required=True)
    batch = fields.Char(string="Batch")