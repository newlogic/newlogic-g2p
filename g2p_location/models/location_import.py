#
# Copyright (c) 2022 Newlogic.
#
# This file is part of newlogic-g2p-erp.
# See https://github.com/newlogic/newlogic-g2p-erp/ for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import base64
import logging
from io import BytesIO

from xlrd import open_workbook

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class G2PLocationImport(models.Model):
    _name = "g2p.location.import"
    _description = "Locations Import Table"

    name = fields.Char("File Name", required=True)
    excel_file = fields.Binary("Location Excel File")
    date_uploaded = fields.Datetime("Date Uploaded")

    upload_id = fields.Many2one("res.users", "Uploaded by")
    date_imported = fields.Datetime("Date Imported")
    import_id = fields.Many2one("res.users", "Imported by")
    date_validated = fields.Datetime("Date Validated")
    validate_id = fields.Many2one("res.users", "Validated by")
    raw_data_ids = fields.One2many(
        "g2p.location.import.raw", "location_import_id", "Raw Data"
    )
    tot_rows_imported = fields.Integer(
        "Total Rows Imported",
        compute="_compute_get_total_rows",
        store=True,
        readonly=True,
    )
    tot_rows_error = fields.Integer(
        "Total Rows with Error",
        compute="_compute_get_total_rows",
        store=True,
        readonly=True,
    )
    state = fields.Selection(
        [
            ("New", "New"),
            ("Uploaded", "Uploaded"),
            ("Imported", "Imported"),
            ("Done", "Done"),
            ("Cancelled", "Cancelled"),
        ],
        "Status",
        readonly=True,
        default="New",
    )

    @api.onchange("excel_file")
    def excel_file_change(self):
        if self.name:
            self.update(
                {
                    "date_uploaded": fields.Datetime.now(),
                    "upload_id": self.env.user,
                    "state": "Uploaded",
                }
            )
        else:
            self.update({"date_uploaded": None, "upload_id": None, "state": "New"})

    @api.depends("raw_data_ids")
    def _compute_get_total_rows(self):
        for rec in self:
            tot_rows_imported = 0
            tot_rows_error = 0
            for ln in rec.raw_data_ids:
                tot_rows_imported += 1
                if ln.state == "Error":
                    tot_rows_error += 1
            rec.update(
                {
                    "tot_rows_imported": tot_rows_imported,
                    "tot_rows_error": tot_rows_error,
                }
            )

    def cancel_import(self):
        for rec in self:
            rec.update({"state": "Cancelled"})

    def import_data(self):  # noqa: C901
        _logger.info("Location Import: Started: %s" % fields.Datetime.now())
        for rec in self:
            _logger.info(
                "Location Import: Loading Excel File: %s" % fields.Datetime.now()
            )
            try:
                inputx = BytesIO()
                inputx.write(base64.decodebytes(rec.excel_file))
                book = open_workbook(file_contents=inputx.getvalue())
            except TypeError as e:
                raise ValidationError("ERROR: {}".format(e))  # noqa: C901
            sheet = book.sheets()[0]
            vals = []
            _logger.info(
                "Location Import: Parsing Excel File: %s" % fields.Datetime.now()
            )

            columns = []

            mainvals = {}
            max_cols = None
            for row in range(sheet.nrows):
                if row == 0:  # Ignore First Row containing column headings
                    for col in range(sheet.ncols):
                        col_name = sheet.cell(0, col).value
                        if col_name.find("Name") >= 0:
                            maxcolsstr = col_name.strip("admin").replace("Name", "")
                            maxcols_name_length = len(maxcolsstr)
                            if maxcols_name_length == 5 or maxcols_name_length == 4:
                                maxcolsstr = maxcolsstr[:-3]
                            try:
                                max_cols = int(maxcolsstr)
                                break
                            except Exception:
                                max_cols = None
                else:
                    if max_cols:
                        xcols = max_cols
                        while xcols >= 0:

                            admin_code = None
                            admin_name = None
                            admin_ref = None
                            admin_alt1 = None
                            admin_alt2 = None
                            state = "Validated"
                            errctr = 0
                            remarks = ""
                            # Loop through the columns
                            lang = {}
                            Languages = self.env["res.lang"].search([('active', "=", True)])
                            for col in range(sheet.ncols):

                                # Get the column value
                                col_value = sheet.cell(row, col).value
                                if col_value == "<Null>":
                                    col_value = ""

                                # Determine the column name based on First Row rowIndex(0), columnIndex(col)
                                col_name = sheet.cell(0, col).value
                                if col_name.find(str(xcols) + "Pcode") >= 0:
                                    admin_code = col_value
                                elif col_name.find(str(xcols) + "Name") >= 0:
                                    if not admin_name:
                                        admin_name = col_value
                                        if not col_value:
                                            errctr += 1
                                            state = "Error"
                                            remarks += (
                                                str(errctr)
                                                + ".) Name cannot be blank; "
                                            )
                                    
                                    for Lang in Languages:
                                        if col_name.find(str(xcols) + "Name_" + Lang.iso_code) >= 0:
                                            lang.update({
                                                Lang.iso_code: {
                                                    'name': col_value,
                                                    'lang_id': Lang.id,
                                                    'iso_code': Lang.iso_code
                                                }
                                            })
                                            
                                    
                                elif col_name.find(str(xcols) + "Ref") >= 0:
                                    admin_ref = col_value
                                elif col_name.find(str(xcols) + "AltName1") >= 0:
                                    admin_alt1 = col_value
                                elif col_name.find(str(xcols) + "AltName2") >= 0:
                                    admin_alt2 = col_value
                                _logger.info(
                                            "Location Masterlist Import: LANGUAGES: %s"
                                            % lang
                                            )
                            lang_ids = []
                            for x in lang:
                                lang_ids.append([0, 0, lang[x]])

                            # Store values to columns
                            columns.append(
                                {
                                    "admin_name": admin_name,
                                    "admin_code": admin_code,
                                    "admin_ref": admin_ref,
                                    "admin_alt1": admin_alt1,
                                    "admin_alt2": admin_alt2,
                                    "level": xcols,
                                    "remarks": remarks,
                                    "state": state,
                                    "row_index": row,
                                    "lang_ids": lang_ids
                                }
                            )

                            xcols -= 1

            for val in columns:
                vals.append([0, 0, val])

            # raise Warning('Debug: %s' % vals)
            _logger.info(
                "Location Masterlist Import: Updating Record: %s"
                % fields.Datetime.now()
            )
            mainvals.update(
                {
                    "date_imported": fields.Datetime.now(),
                    "import_id": self.env.user,
                    "date_validated": fields.Datetime.now(),
                    "validate_id": self.env.user,
                    "state": "Imported",
                    "raw_data_ids": vals,
                }
            )
            rec.update(mainvals)

            _logger.info(
                "Location Masterlist Import: Completed: %s" % fields.Datetime.now()
            )

    def save_to_location(self):
        for rec in self:
            parent_id = None
            for raw in rec.raw_data_ids:
                if raw.state == "Validated":
                    if raw.admin_name:
                        if raw.level == 0:
                            new_vals = {
                                "name": raw.admin_name or False,
                                "code": raw.admin_code or False,
                                "altnames": raw.admin_alt1 or raw.admin_alt2 or False,
                                "level": raw.level or False,
                            }
                        else:
                            new_vals = {
                                "parent_id": parent_id,
                                "name": raw.admin_name or False,
                                "code": raw.admin_code or False,
                                "altnames": raw.admin_alt1 or raw.admin_alt2 or False,
                                "level": raw.level or False,
                            }
                        # Check if Location already Exist
                        curr_location = self.env["g2p.location"].search(
                            [("name", "=", raw.admin_name)]
                        )

                        if not curr_location:
                            location_id = self.env["g2p.location"].create(new_vals)
                            parent_id = location_id.id
                            raw.update({"state": "Posted"})
                        else:
                            location_id = curr_location[0].update(new_vals)
                            parent_id = curr_location[0].id
                            raw.update({"state": "Updated"})
                        for lang in raw.lang_ids:
                            vals_list = []
                            trans_name = lang.name
                            iso_code = lang.lang_id.code
                            vals_list.append({
                                            "name": 'g2p.location,name',
                                            "lang": iso_code,
                                            "res_id": parent_id,
                                            "src":  raw.admin_name,
                                            "value": trans_name,
                                            "state": 'translated',
                                            "type": 'model',
                                            })
                            self.env["ir.translation"]._update_translations(vals_list)
                        rec.update({"state": "Done"})
                    else:
                        raw.update({"state": "Error"})

                else:
                    raw.update({"state": "Error", "remarks": "Incomplete information!"})


# Assets Import Raw Data
class G2PLocationImportActivities(models.Model):
    _name = "g2p.location.import.raw"
    _description = "Location Import Raw Data"
    _order = "row_index, level"

    location_import_id = fields.Many2one(
        "g2p.location.import", "Location Import", required=True
    )
    admin_name = fields.Char("Admin Name")
    admin_code = fields.Char("Admin Code")
    admin_alt1 = fields.Char("Admin Alt1")
    admin_alt2 = fields.Char("Admin Alt2")
    admin_ref = fields.Char("Admin Ref")
    level = fields.Integer("Level")
    row_index = fields.Integer("Row Index")
    lang_ids = fields.One2many(
        "g2p.location.import.lang", "raw_id", "Languages")
    remarks = fields.Text("Remarks/Errors")
    state = fields.Selection(
        [
            ("New", "New"),
            ("Validated", "Validated"),
            ("Error", "Error"),
            ("Updated", "Updated"),
            ("Posted", "Posted"),
        ],
        "Status",
        readonly=True,
        default="New",
    )
class G2PLocationImportRawLanguages(models.Model):
    _name = "g2p.location.import.lang"
    _description = "Location Import Raw Data Languages"

    name = fields.Char("Translate Name")
    raw_id = fields.Many2one("g2p.location.import.raw", "Location Raw ID")
    lang_id = fields.Many2one("res.lang", "Languages")

    iso_code = fields.Char("ISO Code")