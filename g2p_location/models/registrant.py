# -*- coding: utf-8 -*-

from odoo import fields, models

class G2PRegistrant(models.Model):
    _inherit = 'res.partner'

    #Custom Fields
    location_id = fields.Many2one('g2p.location','Location')
