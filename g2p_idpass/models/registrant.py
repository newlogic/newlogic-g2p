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

import logging
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class G2PRegistrant(models.Model):
    _name = "res.partner"
    _inherit = [_name, "mail.thread"]

    id_pdf = fields.Binary("ID PASS")
    id_pdf_filename = fields.Char("ID File Name")

    def send_idpass_parameters(self):
        issue_date = datetime.today().strftime("%Y/%m/%d")
        expiry_date = datetime.today() + relativedelta(years=2)
        expiry_date = expiry_date.strftime("%Y/%m/%d")
        # TODO: JJ - Find a good way to generate ID document number
        identification_no = f"{self.id:06d}"
        data = {
            "fields": {
                "date_of_expiry": expiry_date,
                "date_of_issue": issue_date,
                "given_names": self.given_name,
                "identification_no": identification_no,
                "nationality": "Filipino",
                "place_of_birth": self.birth_place or "",
                "sex": self.gender or "",
                "surname": self.family_name,
                "qrcode_svg_1": f"{identification_no};{self.given_name};{self.family_name}",
            }
        }
        data_str = str(data).replace("'", '"')
        _logger.info("ID PASS Data: %s" % data_str)

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.post(
            "https://idpass-backend.newlogic-demo.com/api/v1/cards/f45614d2-796d-4749-8358-4318cfa19edb/render/",
            headers=headers,
            data=data_str,
        )
        if response.status_code == 200:
            pdf_vals = response.json()
            file_pdf = pdf_vals["files"]["pdf"]
            file_pdf = file_pdf[28:]
            self.id_pdf = file_pdf
            self.id_pdf_filename = (
                "ID PASS - "
                + self.name.strip()
                + " ("
                + datetime.today().strftime("%Y/%m/%d")
                + ").pdf"
            )

            attachment = self.env["ir.attachment"].create(
                {
                    "name": self.id_pdf_filename,
                    "type": "binary",
                    "datas": file_pdf,
                    "res_model": self._name,
                    "res_id": self.id,
                    "mimetype": "application/x-pdf",
                }
            )

            attachment_id = {attachment.id}
            model_id = self.env["res.partner"].search([("id", "=", self.id)])
            msg_body = "Generated ID: " + self.id_pdf_filename
            model_id.message_post(body=msg_body, attachment_ids=attachment_id)
        else:
            raise ValidationError(
                _(
                    "ID PASS Error: %s Code: %s"
                    % (response.reason, response.status_code)
                )
            )  # noqa: C901
        _logger.info(
            "ID PASS Response: %s Code: %s" % (response.reason, response.status_code)
        )
        return
