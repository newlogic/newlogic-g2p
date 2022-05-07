# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _

from odoo.exceptions import AccessError, UserError, ValidationError, Warning

class G2PRegistrantRelationship(models.Model):
    _name = 'g2p.reg.rel'
    _description = 'Registrant Relationship'
    _order = 'id desc'

    registrant1 = fields.Many2one('res.partner','Registrant 1')
    registrant2 = fields.Many2one('res.partner','Registrant 2')
    relation = fields.Many2one('g2p.relationship','Relation')
    disabled = fields.Datetime('Date Disabled')
    disabled_by = fields.Many2one('res.users', 'Disabled by')
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')

    def name_get(self):
        res = super(G2PRegistrantRelationship, self).name_get()
        for rec in self:
            name = ''
            if rec.registrant1:
                name += rec.registrant1.name
            if rec.registrant2:
                name += ' / ' + rec.registrant2.name
            res.append((rec.id, name))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args = ['|',('registrant1', operator, name),('registrant2', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

class G2PRelationship(models.Model):
    _name = 'g2p.relationship'
    _description = 'Relationship'
    _order = 'id desc'

    name = fields.Char('Name')
    bidirectional = fields.Boolean('Bi-directional')
    reverse_name = fields.Char('Reverse Name')