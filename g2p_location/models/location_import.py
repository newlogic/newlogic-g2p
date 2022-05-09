# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from xlrd import open_workbook
import base64
from io import BytesIO

import logging
_logger = logging.getLogger(__name__)

#Location Import
class G2PLocationImport(models.Model):
    _name = "g2p.location.import"
    _description = 'Locations Import Table'

    name = fields.Char ('File Name', required=True)
    excel_file = fields.Binary('Location Excel File')
    date_uploaded = fields.Datetime('Date Uploaded')

    models_ids = fields.Many2many ('ibspro.ref.models',string='Models')

    upload_id = fields.Many2one('res.users','Uploaded by')
    date_imported = fields.Datetime('Date Imported')
    import_id = fields.Many2one('res.users','Imported by')
    date_validated = fields.Datetime('Date Validated')
    validate_id = fields.Many2one('res.users','Validated by')
    raw_data_ids = fields.One2many('g2p.location.import.raw','location_import_id','Raw Data')
    tot_rows_imported = fields.Integer('Total Rows Imported', compute='_get_total_rows', store=True, readonly=True)
    tot_rows_error = fields.Integer('Total Rows with Error', compute='_get_total_rows', store=True, readonly=True)
    state = fields.Selection([('New','New'),('Uploaded','Uploaded'),('Imported','Imported'),('Done','Done'),('Cancelled','Cancelled')],'Status',readonly=True,default='New')
    
    @api.onchange('excel_file')
    def excel_file_change(self):
        if self.name:
            self.update({'date_uploaded':fields.Datetime.now(),'upload_id':self.env.user,'state':'Uploaded'})
        else:
            self.update({'date_uploaded':None,'upload_id':None,'state':'New'})

    @api.depends('raw_data_ids')
    def _get_total_rows(self):
        for rec in self:
            tot_rows_imported = 0
            tot_rows_error = 0
            for ln in rec.raw_data_ids:
                tot_rows_imported += 1
                if ln.state == 'Error':
                    tot_rows_error += 1
            rec.update({'tot_rows_imported':tot_rows_imported, 'tot_rows_error':tot_rows_error})

    def cancel_import(self):
        for rec in self:
            rec.update({'state':'Cancelled'})

    def import_data(self):
        _logger.info('Location Import: Started: %s' % fields.Datetime.now())
        for rec in self:
            _logger.info('Location Import: Loading Excel File: %s' % fields.Datetime.now())
            try:
                inputx = BytesIO()
                inputx.write(base64.decodebytes(rec.excel_file))
                book = open_workbook(file_contents=inputx.getvalue())
            except TypeError as e:
                raise ValidationError(u'ERROR: {}'.format(e))
            sheet = book.sheets()[0]
            vals = []
            _logger.info('Location Import: Parsing Excel File: %s' % fields.Datetime.now())
            for i in range(sheet.nrows):
                if i == 0:
                    continue

                admin0_name = sheet.cell(i, 11).value
                admin0_code = sheet.cell(i, 12).value
                admin1_name = sheet.cell(i, 9).value
                admin1_code = sheet.cell(i, 10).value
                admin2_name = sheet.cell(i, 7).value
                admin2_code = sheet.cell(i, 8).value
                admin3_name = sheet.cell(i, 2).value
                admin3_code = sheet.cell(i, 3).value
                admin3_ref = sheet.cell(i, 4).value
                admin3_alt1 = sheet.cell(i, 5).value
                admin3_alt2 = sheet.cell(i, 6).value

                _logger.info('Assets Import: Started: [%s] %s' % (admin0_name, fields.Datetime.now()))

                #Data validation
                state = 'Validated'
                errctr = 0
                remarks = ''
                mainvals = {}

                if not admin0_name:
                    errctr += 1
                    state = 'Error'
                    remarks += str(errctr) + '.) Name cannot be blank; '

                if not admin1_name:
                    errctr += 1
                    state = 'Error'
                    remarks += str(errctr) + '.) Name cannot be blank; '

                if not admin2_name:
                    errctr += 1
                    state = 'Error'
                    remarks += str(errctr) + '.) Name cannot be blank; '

                if not admin3_name:
                    errctr += 1
                    state = 'Error'
                    remarks += str(errctr) + '.) Name cannot be blank; '
                
                if admin0_name == "<NULL>" or admin0_name == "NULL" or admin0_name == "<Null>":
                    admin0_name = ""
                
                if admin0_code == "<NULL>" or admin0_code == "NULL" or admin0_code == "<Null>":
                    admin0_code = ""
                
                if admin1_name == "<NULL>" or admin1_name == "NULL" or admin1_name == "<Null>":
                    admin1_name = ""
                
                if admin1_code == "<NULL>" or admin1_code == "NULL" or admin1_code == "<Null>":
                    admin1_code = ""
                
                if admin2_name == "<NULL>" or admin2_name == "NULL" or admin2_name == "<Null>":
                    admin2_name = ""
                
                if admin2_code == "<NULL>" or admin2_code == "NULL" or admin2_code == "<Null>":
                    admin2_code = ""
                
                if admin3_name == "<NULL>" or admin3_name == "NULL" or admin3_name == "<Null>":
                    admin3_name = ""
                
                if admin3_code == "<NULL>" or admin3_code == "NULL" or admin3_code == "<Null>":
                    admin3_code = ""
                
                if admin3_ref == "<NULL>" or admin3_ref == "NULL" or admin3_ref == "<Null>":
                    admin3_ref = ""
                
                if admin3_alt1 == "<NULL>" or admin3_alt1 == "NULL" or admin3_alt1 == "<Null>":
                    admin3_alt1 = ""
                
                if admin3_alt2 == "<NULL>" or admin3_alt2 == "NULL" or admin3_alt2 == "<Null>":
                    admin3_alt2 = ""




                

                ######################################

                vals.append([0,0,{
                    'admin0_name': admin0_name,
                    'admin0_code': admin0_code,
                    'admin1_name': admin1_name,
                    'admin1_code': admin1_code,
                    'admin2_name': admin2_name,
                    'admin2_code': admin2_code,
                    'admin3_name': admin3_name,
                    'admin3_code': admin3_code,
                    'admin3_ref': admin3_ref,
                    'admin3_alt1': admin3_alt1,
                    'admin3_alt2': admin3_alt2,
                    'remarks': remarks,
                    'state': state,
                }])
            #raise Warning('Debug: %s' % vals)
            _logger.info('Location Masterlist Import: Updating Record: %s' % fields.Datetime.now())
            mainvals.update({
                'date_imported':fields.Datetime.now(),
                'import_id':self.env.user,
                'date_validated':fields.Datetime.now(),
                'validate_id':self.env.user,
                'state':'Imported',
                'raw_data_ids':vals,
            })
            rec.update(mainvals)
        _logger.info('Location Masterlist Import: Completed: %s' % fields.Datetime.now())

    def save_to_location(self):
        for rec in self:
            for raw in rec.raw_data_ids:
                if raw.state == 'Validated':
                    if raw.admin0_name:
                        curr_location = self.env['g2p.location'].search([('name','=',raw.admin0_name)])
                        if not curr_location:
                            new_vals = {
                                'name' : raw.admin0_name or False,
                                'code' : raw.admin0_code or False,
                            }
                            new_location = self.env['g2p.location'].create(new_vals)
                            curr_parent_location = new_location.id
                            if raw.admin1_name:
                                curr_child_location1 = self.env['g2p.location'].search([('name','=',raw.admin1_name)])
                                if not curr_child_location1:
                                    child_vals = {
                                        'parent_id' : curr_parent_location,
                                        'name' : raw.admin1_name or False,
                                        'code' : raw.admin1_code or False,
                                    }
                                    new_child_location1 = self.env['g2p.location'].create(child_vals)
                                    curr_parent_location1 = new_child_location1.id
                                    if raw.admin2_name:
                                        curr_child_location2 = self.env['g2p.location'].search([('name','=',raw.admin2_name)])
                                        if not curr_child_location2:
                                            child_vals = {
                                                'parent_id' : curr_parent_location1,
                                                'name' : raw.admin2_name or False,
                                                'code' : raw.admin2_code or False,
                                            }
                                            new_child_location2 = self.env['g2p.location'].create(child_vals)
                                            curr_parent_location2 = new_child_location2.id
                                            if raw.admin3_name:
                                                curr_child_location3 = self.env['g2p.location'].search([('name','=',raw.admin3_name)])
                                                if not curr_child_location3:
                                                    child_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name or False,
                                                        'code' : raw.admin3_code or False,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    new_child_location3 = self.env['g2p.location'].create(child_vals)
                                                    curr_parent_location3 = new_child_location3.id
                                                else:
                                                    new_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name,
                                                        'code' : raw.admin3_code,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    curr_child_location3[0].update(new_vals)
                                        else:
                                            new_vals = {
                                                'parent_id' : curr_parent_location1,
                                                'name' : raw.admin2_name,
                                                'code' : raw.admin2_code,
                                            }
                                            curr_child_location2[0].update(new_vals)
                                            curr_parent_location2 = curr_child_location2[0].id
                                            if raw.admin3_name:
                                                curr_child_location3 = self.env['g2p.location'].search([('name','=',raw.admin3_name)])
                                                if not curr_child_location3:
                                                    child_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name or False,
                                                        'code' : raw.admin3_code or False,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    new_child_location3 = self.env['g2p.location'].create(child_vals)
                                                    curr_parent_location3 = new_child_location3.id
                                                else:
                                                    new_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name,
                                                        'code' : raw.admin3_code,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    curr_child_location3[0].update(new_vals)
                                            

                                else:
                                    new_vals = {
                                        'parent_id' : curr_parent_location,
                                        'name' : raw.admin1_name,
                                        'code' : raw.admin1_code,
                                    }
                                    curr_child_location1[0].update(new_vals)
                                    curr_parent_location1 = curr_child_location1[0].id
                                    if raw.admin2_name:
                                        curr_child_location2 = self.env['g2p.location'].search([('name','=',raw.admin2_name)])
                                        if not curr_child_location2:
                                            child_vals = {
                                                'parent_id' : curr_parent_location1,
                                                'name' : raw.admin2_name or False,
                                                'code' : raw.admin2_code or False,
                                            }
                                            new_child_location2 = self.env['g2p.location'].create(child_vals)
                                            curr_parent_location2 = new_child_location2.id
                                            if raw.admin3_name:
                                                curr_child_location3 = self.env['g2p.location'].search([('name','=',raw.admin3_name)])
                                                if not curr_child_location3:
                                                    child_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name or False,
                                                        'code' : raw.admin3_code or False,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    new_child_location3 = self.env['g2p.location'].create(child_vals)
                                                    curr_parent_location3 = new_child_location3.id
                                                else:
                                                    new_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name,
                                                        'code' : raw.admin3_code,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    curr_child_location3[0].update(new_vals)
                                        else:
                                            new_vals = {
                                                'parent_id' : curr_parent_location1,
                                                'name' : raw.admin2_name,
                                                'code' : raw.admin2_code,
                                            }
                                            curr_child_location2[0].update(new_vals)
                                            curr_parent_location2 = curr_child_location2[0].id
                                            if raw.admin3_name:
                                                curr_child_location3 = self.env['g2p.location'].search([('name','=',raw.admin3_name)])
                                                if not curr_child_location3:
                                                    child_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name or False,
                                                        'code' : raw.admin3_code or False,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    new_child_location3 = self.env['g2p.location'].create(child_vals)
                                                    curr_parent_location3 = new_child_location3.id
                                                else:
                                                    new_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name,
                                                        'code' : raw.admin3_code,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    curr_child_location3[0].update(new_vals)
                        
                        else:
                            new_vals = {
                                'name' : raw.admin0_name,
                                'code' : raw.admin0_code,
                            }
                            curr_location[0].update(new_vals)
                            curr_parent_location = curr_location[0].id
                            if raw.admin1_name:
                                curr_child_location1 = self.env['g2p.location'].search([('name','=',raw.admin1_name)])
                                if not curr_child_location1:
                                    child_vals = {
                                        'parent_id' : curr_parent_location,
                                        'name' : raw.admin1_name or False,
                                        'code' : raw.admin1_code or False,
                                    }
                                    new_child_location1 = self.env['g2p.location'].create(child_vals)
                                    curr_parent_location1 = new_child_location1.id
                                    if raw.admin2_name:
                                        curr_child_location2 = self.env['g2p.location'].search([('name','=',raw.admin2_name)])
                                        if not curr_child_location2:
                                            child_vals = {
                                                'parent_id' : curr_parent_location1,
                                                'name' : raw.admin2_name or False,
                                                'code' : raw.admin2_code or False,
                                            }
                                            new_child_location2 = self.env['g2p.location'].create(child_vals)
                                            curr_parent_location2 = new_child_location2.id
                                            if raw.admin3_name:
                                                curr_child_location3 = self.env['g2p.location'].search([('name','=',raw.admin3_name)])
                                                if not curr_child_location3:
                                                    child_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name or False,
                                                        'code' : raw.admin3_code or False,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    new_child_location3 = self.env['g2p.location'].create(child_vals)
                                                    curr_parent_location3 = new_child_location3.id
                                                else:
                                                    new_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name,
                                                        'code' : raw.admin3_code,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    curr_child_location3[0].update(new_vals)
                                        else:
                                            new_vals = {
                                                'parent_id' : curr_parent_location1,
                                                'name' : raw.admin2_name,
                                                'code' : raw.admin2_code,
                                            }
                                            curr_child_location2[0].update(new_vals)
                                            curr_parent_location2 = curr_child_location2[0].id
                                            if raw.admin3_name:
                                                curr_child_location3 = self.env['g2p.location'].search([('name','=',raw.admin3_name)])
                                                if not curr_child_location3:
                                                    child_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name or False,
                                                        'code' : raw.admin3_code or False,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    new_child_location3 = self.env['g2p.location'].create(child_vals)
                                                    curr_parent_location3 = new_child_location3.id
                                                else:
                                                    new_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name,
                                                        'code' : raw.admin3_code,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    curr_child_location3[0].update(new_vals)
                                            

                                else:
                                    new_vals = {
                                        'parent_id' : curr_parent_location,
                                        'name' : raw.admin1_name,
                                        'code' : raw.admin1_code,
                                    }
                                    curr_child_location1[0].update(new_vals)
                                    curr_parent_location1 = curr_child_location1[0].id
                                    if raw.admin2_name:
                                        curr_child_location2 = self.env['g2p.location'].search([('name','=',raw.admin2_name)])
                                        if not curr_child_location2:
                                            child_vals = {
                                                'parent_id' : curr_parent_location1,
                                                'name' : raw.admin2_name or False,
                                                'code' : raw.admin2_code or False,
                                            }
                                            new_child_location2 = self.env['g2p.location'].create(child_vals)
                                            curr_parent_location2 = new_child_location2.id
                                            if raw.admin3_name:
                                                curr_child_location3 = self.env['g2p.location'].search([('name','=',raw.admin3_name)])
                                                if not curr_child_location3:
                                                    child_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name or False,
                                                        'code' : raw.admin3_code or False,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    new_child_location3 = self.env['g2p.location'].create(child_vals)
                                                    curr_parent_location3 = new_child_location3.id
                                                else:
                                                    new_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name,
                                                        'code' : raw.admin3_code,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    curr_child_location3[0].update(new_vals)
                                        else:
                                            new_vals = {
                                                'parent_id' : curr_parent_location1,
                                                'name' : raw.admin2_name,
                                                'code' : raw.admin2_code,
                                            }
                                            curr_child_location2[0].update(new_vals)
                                            curr_parent_location2 = curr_child_location2[0].id
                                            if raw.admin3_name:
                                                curr_child_location3 = self.env['g2p.location'].search([('name','=',raw.admin3_name)])
                                                if not curr_child_location3:
                                                    child_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name or False,
                                                        'code' : raw.admin3_code or False,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    new_child_location3 = self.env['g2p.location'].create(child_vals)
                                                    curr_parent_location3 = new_child_location3.id
                                                else:
                                                    new_vals = {
                                                        'parent_id' : curr_parent_location2,
                                                        'name' : raw.admin3_name,
                                                        'code' : raw.admin3_code,
                                                        'altnames' : raw.admin3_alt1 or raw.admin3_alt2 or False,
                                                    }
                                                    curr_child_location3[0].update(new_vals)
                        
                        raw.update({'state':'Posted'})
                        rec.update({'state':'Done'})
                    else:
                        raw.update({'state':'Error','remarks':'Incomplete information!'})


#Assets Import Raw Data
class G2PLocationImportActivities(models.Model):
    _name = "g2p.location.import.raw"
    _description = 'Location Import Raw Data'
    _order = 'id'

    location_import_id = fields.Many2one ('g2p.location.import', 'Location Import', required=True)
    admin0_name = fields.Char('Admin 0 Name')
    admin0_code = fields.Char('Admin 0 Code')
    admin0_alt = fields.Char('Admin 0 Alt')
    admin1_name = fields.Char('Admin 1 Name')
    admin1_code = fields.Char('Admin 1 Code')
    admin1_alt = fields.Char('Admin 1 Alt')
    admin2_name = fields.Char('Admin 2 Name')
    admin2_code = fields.Char('Admin 2 Code')
    admin2_alt = fields.Char('Admin 2 Alt')
    admin3_name = fields.Char('Admin 3 Name')
    admin3_code = fields.Char('Admin 3 Code')
    admin3_alt1 = fields.Char('Admin 3 Alt1')
    admin3_alt2 = fields.Char('Admin 3 Alt2')
    admin3_ref = fields.Char('Admin 3 Ref')

    remarks = fields.Text('Remarks/Errors')
    state = fields.Selection([('New','New'),('Validated','Validated'),('Error','Error'),('No Model','No Model'),('No WBS','No WBS'),('No Activity','No Activity'),('Posted','Posted')],'Status',readonly=True,default='New')


