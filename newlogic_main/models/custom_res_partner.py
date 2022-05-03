# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class CustomResPartner(models.Model):
    _inherit = 'res.partner'

    #Custom Fields
    date_disabled = fields.Datetime('Date Disabled', tracking=True)
    reason_disabled = fields.Text('Reason for disabling')
    userid_disabled = fields.Many2one('res.users', 'Disabled by', tracking=True)

    #Individuals
    family_name = fields.Char('Family Name', tracking=True)
    given_name = fields.Char('Given Name', tracking=True)
    addl_name = fields.Char('Additional Name', tracking=True)
    birth_place = fields.Char('Birth Place')
    birthdate = fields.Date('Date of Birth', tracking=True)
    age = fields.Char(compute='_calc_age', string="Age", size= 50,readonly=True)
    gender = fields.Selection([('Female','Female'),('Male','Male'),('Other','Other')],'Gender', tracking=True)

    registrant = fields.Boolean('Registrant')
    
    @api.depends('birthdate')
    def _calc_age(self):
        for line in self:
            line.age = self.compute_age_from_dates(line.birthdate)

    def compute_age_from_dates(self, partner_dob):
        #now=datetime.strptime(fields.Datetime.now()[:10],'%Y-%m-%d')
        now=datetime.strptime(str(fields.Datetime.now())[:10],'%Y-%m-%d')
        if (partner_dob):
            #dob=datetime.strftime(partner_dob,'%Y-%m-%d')
            dob = partner_dob
            delta = relativedelta (now, dob)
            #years_months_days = str(delta.years) +"y "+ str(delta.months) +"m "+ str(delta.days)+"d"
            years_months_days = str(delta.years)
        else:
            years_months_days = "No Birthdate!"
        return years_months_days

    @api.onchange('registrant','family_name','given_name','addl_name')
    def partner_name_change(self):
        vals = {}
        if self.registrant:
            name = ''
            if self.family_name:
                name += self.family_name + ', '
            if self.given_name:
                name += self.given_name + ' '
            if self.addl_name:
                name += self.addl_name + ' '

            vals.update({'name': name.upper()})
        self.update(vals)