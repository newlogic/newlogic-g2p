# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class G2PRegistrantRelationship(models.Model):
    _name = 'g2p.reg.rel'
    _description = 'Registrant Relationship'
    _order = 'id desc'

    registrant1 = fields.Many2one('res.partner','Registrant 1')
    registrant2 = fields.Many2one('res.partner','Registrant 2')
    relation = fields.Many2one('g2p.relationship','Relation')
    disabled = fields.Datetime('Date Disabled')
    disabled_by = fields.Many2one('res.users', 'Disabled by')

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
