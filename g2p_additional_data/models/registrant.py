# -*- coding: utf-8 -*-

from odoo import fields, models

class G2PRegistrant(models.Model):
    _inherit = 'res.partner'

    #Custom Fields
    additional_data_ids = fields.One2many('g2p.registrant.additional.data', 'registrant_id', string="Additional Data")
    registration_source_id = fields.Many2one('g2p.datasource', 'Registration Source')
