# -*- coding: utf-8 -*-

from odoo import fields, models

class G2PLocation(models.Model):
    _name = 'g2p.location'
    _description = 'Location'
    _order = 'id desc'

    parent_id = fields.Many2one('g2p.location', 'Parent')
    name = fields.Char('Name', required=True, translate=True)
    code = fields.Char('Code')
    altnames = fields.Char('Alternate Name')
    level = fields.Integer('Level')
    child_ids = fields.One2many('g2p.location', 'id', "Child", compute="_get_childs")

    def _get_childs(self):
        for rec in self:
            child_ids = self.env['g2p.location'].search([('parent_id','=',rec.id)])
            rec.child_ids = child_ids

