# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class LMSActivityScheduleTransfer(models.TransientModel):
    _name = 'esmis.lms.activity.transfer.wizard'
    _description = 'LMS Activities Transfer Wizard'

    @api.model
    def default_get(self, fields):
        res = super(LMSActivityScheduleTransfer, self).default_get(fields)
        if (not fields or 'lms_act_id' in fields) and 'lms_act_id' not in res:
            if self.env.context.get('active_id'):
                res['lms_act_id'] = self.env.context['active_id']
            curr_sy_term = self.env['esmis.enrollment.syterms'].sudo().search([('current','=',True)], limit=1)
            curr_sy_term_id = None
            if curr_sy_term:
                curr_sy_term_id = curr_sy_term.id
            res['curr_sy_term_id'] = curr_sy_term_id
        return res

    name = fields.Date('Transfer to Date',required=True)
    lms_act_id = fields.Many2one('esmis.hr.sched.cal.lms.view','LMS Activity')
    sched_id = fields.Many2one('esmis.hr.sched.cal','Faculty Schedule', required=True)
    curr_sy_term_id = fields.Many2one('esmis.enrollment.syterms','Current School Year - Term')

    @api.onchange('name')
    def _onchange_name(self):
        if self.name and self.lms_act_id:
            date_sched = self.name
            employee_id = self.lms_act_id.employee_id.id
            sy_term_id = self.curr_sy_term_id.id
            sched_cal_ids = self.env['esmis.hr.sched.cal'].search([('date_sched','=',date_sched),('sy_term_id','=',sy_term_id),('employee_id','=',employee_id)])
            if sched_cal_ids:
                return {'domain': {'sched_id': [('id', 'in', sched_cal_ids.mapped('id'))]}}

    def action_transfer_activity(self):
        for rec in self:
            if rec.name and rec.sched_id:
                employee_id = rec.lms_act_id.employee_id.id
                subj_code = rec.lms_act_id.subj_code
                subj_name = rec.lms_act_id.subj_name
                log_readable = rec.lms_act_id.log_readable
                sched_id = rec.sched_id.id
                lms_mon_obj = self.env['esmis.hr.lms.mon']
                lms_mon_recs = lms_mon_obj.sudo().search([('sched_id','=',False),('employee_id','=',employee_id),('subj_code','=',subj_code),('subj_name','=',subj_name),('log_readable','=',log_readable)])
                if lms_mon_recs:
                    lms_mon_ids = lms_mon_recs.mapped('id')
                    #raise UserError('Debug: %s' % lms_mon_ids)
                    lms_mon_recs.sudo().update({'sched_id':sched_id})
                else:
                    raise UserError('ERROR! There are no unassigned activities associated with the LMS log you selected.')
            else:
                raise UserError('ERROR! The transfer date and Faculty schedule fields must be properly filled-up.')