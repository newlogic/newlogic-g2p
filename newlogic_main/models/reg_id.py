# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _

from odoo.exceptions import AccessError, UserError, ValidationError, Warning

class G2PRegistrantID(models.Model):
    _name = 'g2p.reg.id'
    _description = 'Registrant ID'
    _order = 'id desc'

    registrant = fields.Many2one('res.partner','Registrant')
    id_type = fields.Many2one('g2p.id.type','ID Type')
    value = fields.Char('Value', size=100)

    def name_get(self):
        res = super(G2PRegistrantID, self).name_get()
        for rec in self:
            name = ''
            if rec.registrant:
                name = rec.registrant.name
            res.append((rec.id, name))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args = [('registrant', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

class G2PIDType(models.Model):
    _name = 'g2p.id.type'
    _description = 'ID Type'
    _order = 'id desc'

    name = fields.Char('Name')

