# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class RegIndividuals(models.Model):
    _name = 'nl.reg.individual'
    _description = "Individual Registrant"
    _order = 'id desc'

    name = fields.Char('Full Name')
    family_name = fields.Char('Family Name', tracking=True)
    given_name = fields.Char('Given Name', tracking=True)
    addl_name = fields.Char('Additional Name', tracking=True)
    birth_place = fields.Char('Birth Place')
    birthdate = fields.Date('Date of Birth', tracking=True)
    age = fields.Char(compute='_calc_age', string="Age", size= 50,readonly=True)
    gender = fields.Selection([('Female','Female'),('Male','Male'),('Other','Other')],'Gender', tracking=True)

    @api.onchange('family_name','given_name','addl_name')
    def name_change(self):
        vals = {}
        name = ''
        if self.family_name:
            name += self.family_name + ', '
        if self.given_name:
            name += self.given_name + ' '
        if self.addl_name:
            name += self.addl_name + ' '
        vals.update({'name': name.upper()})
        self.update(vals)

    @api.depends('birthdate')
    def _calc_age(self):
        for line in self:
            line.age = self.compute_age_from_dates(line.birthdate)

    def compute_age_from_dates(self, partner_dob):
        now=datetime.strptime(str(fields.Datetime.now())[:10],'%Y-%m-%d')
        if (partner_dob):
            dob = partner_dob
            delta = relativedelta (now, dob)
            #years_months_days = str(delta.years) +"y "+ str(delta.months) +"m "+ str(delta.days)+"d"
            years_months_days = str(delta.years)
        else:
            years_months_days = "No Birthdate!"
        return years_months_days

