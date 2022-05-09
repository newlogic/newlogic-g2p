# -*- coding: utf-8 -*-

from odoo import fields, models

class G2PAdditionalData(models.Model):
    _name = 'g2p.additional.data'
    _description = "Additional Data Object"
    _order = 'id desc'

    
    source_id = fields.Many2one('g2p.datasource', 'Source')
    name = fields.Char(string="Name")
    json = fields.Text('JSON')
    tag_ids = fields.Many2many('g2p.additional.data.tags', string='Tag')
    editurl = fields.Char(string="Edit URL")
    viewurl = fields.Char(string="View URL")