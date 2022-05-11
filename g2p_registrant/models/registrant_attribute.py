# -*- coding: utf-8 -*-
#################################################################################
#   Copyright 2022 Newlogic
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#################################################################################
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

class RegistrantAttribute(models.Model):
    _name = "g2p.reg.attribute"
    _description = "Registrant Attribute"
    _order = 'sequence, id'
    _inherit = ['mail.thread']

    name = fields.Char('Attribute', required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, tracking=True)
    value_ids = fields.One2many('g2p.reg.attribute.value', 'attribute_id', 'Values', copy=True)
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    kind = fields.Selection([('int','Integer'),('char','Char'),('text','Text'),('date','Date'),('boolean','Boolean'),('float','Float')], 'Kind', default='char', required=True, tracking=True)
    visible = fields.Selection([('all','All'),('reg','Registrant'),('grp','Group')], 'Visible', default='reg', required=True, tracking=True)


class RegistrantAttributeValue(models.Model):
    _name = "g2p.reg.attribute.value"
    _order = 'attribute_id, sequence, id'
    _description = 'Attribute Value'

    name = fields.Char(string='Value', required=True, translate=True)
    partner_id = fields.Many2one('res.partner', 'Registrant', help="A beneficiary", required=True, domain=[('is_registrant','=',True)])
    attribute_id = fields.Many2one('g2p.reg.attribute', string="Attribute", ondelete='cascade', required=True, index=True)
    sequence = fields.Integer(help="Determine the display order")
    
    value_int = fields.Integer(string='Integer Value', help="Optional field", index=True)
    value_char = fields.Char(string='Char Value', index=True)
    value_text = fields.Text(string='Text Value', help="Optional field")
    value_float = fields.Float(string='Float Value', help="Optional field", index=True)
    value_date = fields.Date(string='Date Value', help="Optional field", index=True)
    value_boolean = fields.Boolean(string='Boolean Value', help="Optional field", index=True)

    kind = fields.Selection([('int','Integer'),('char','Char'),('text','Text'),('date','Date'),('boolean','Boolean'),('float','Float')], 
        'Kind', related='attribute_id.kind')
    visible = fields.Selection([('all','All'),('reg','Registrant'),('grp','Group')], 'Visible', 
        related='attribute_id.visible')

    @api.onchange('visible')
    def onchange_visible(self):
        domain = {}
        if self.visible == 'all':
            domain = {'partner_id': [('is_registrant','=',True)]}
        elif self.visible == 'reg':
            domain = {'partner_id': [('is_registrant','=',True),('is_group','=',False)]}
        elif self.visible == 'grp':
            domain = {'partner_id': [('is_registrant','=',True),('is_group','=',True)]}
        return {
            'domain': domain,
        }

    @api.onchange('kind','value_int','value_char','value_text','value_float','value_date','value_boolean')
    def on_change_value(self):
        val = None
        if self.kind == 'int':
            val = str(self.value_int)
        elif self.kind == 'char':
            val = self.value_char
        elif self.kind == 'text':
            val = self.value_text
        elif self.kind == 'date':
            val = self.value_date
        elif self.kind == 'boolean':
            val = 'TRUE' if self.value_boolean else 'FALSE'
        elif self.kind == 'float':
            val = str(self.value_float)
        self.name = val

    # TODO: One value should be filled at least