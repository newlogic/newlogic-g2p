# -*- coding: utf-8 -*-

from odoo import fields, models

class G2PRegistrantAdditionalData(models.Model):
    _name = 'g2p.registrant.additional.data'
    _description = "Registrant Additional Data"
    _order = 'id desc'

    registrant = fields.Many2one('res.partner', 'Registrant')
    data = fields.Many2one('g2p.additional.data', 'Data')
    json_path = fields.Text('JSON Path')