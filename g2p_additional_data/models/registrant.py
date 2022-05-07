# -*- coding: utf-8 -*-

from odoo import fields, models

class G2PRegistrant(models.Model):
    _inherit = 'res.partner'

    #Custom Fields
    additional_data = fields.One2many('g2p.registrant.additional.data', 'registrant', string="Additional Data")
