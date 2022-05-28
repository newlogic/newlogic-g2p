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

    def send_idpass_parameters(self):  # noqa: C901
        id_pass_param = self.env["g2p.id.pass"].search([("is_active", "=", True)])
        if id_pass_param:

            given_name = self.given_name
            identification_no = f"{self.id:06d}"
            birth_place = self.birth_place or ""
            gender = self.gender or ""
            surname = self.family_name
            full_name = self.name
            if self.is_group:
                head_id = 0
                for group_member in self.group_membership_ids:
                    for member_kind in group_member.kind:
                        if member_kind.is_unique:
                            head_id = group_member.individual.id
                            break
                    if head_id > 0:
                        break
                if head_id > 0:
                    head_registrant = self.env["res.partner"].search(
                        [("id", "=", head_id)]
                    )
                    given_name = head_registrant.given_name
                    identification_no = f"{head_registrant.id:06d}"
                    birth_place = head_registrant.birth_place or ""
                    gender = head_registrant.gender or ""
                    surname = head_registrant.family_name
                    full_name = head_registrant.name
                else:
                    raise ValidationError(
                        _(
                            "ID PASS Error: No Head or Principal Recipient assigned to this Group"
                        )
                    )  # noqa: C901

            issue_date = datetime.today().strftime("%Y/%m/%d")

            expiry_date = datetime.today()

            if id_pass_param[0].expiry_length_type == "years":
                expiry_date = datetime.today() + relativedelta(
                    years=id_pass_param[0].expiry_length
                )
            elif id_pass_param[0].expiry_length_type == "months":
                expiry_date = datetime.today() + relativedelta(
                    months=id_pass_param[0].expiry_length
                )
            else:
                expiry_date = datetime.today() + relativedelta(
                    days=id_pass_param[0].expiry_length
                )

            expiry_date = expiry_date.strftime("%Y/%m/%d")
            # TODO: JJ - Find a good way to generate ID document number

            data = {
                "fields": {
                    "date_of_expiry": expiry_date,
                    "date_of_issue": issue_date,
                    "given_names": given_name,
                    "identification_no": identification_no,
                    "nationality": "Filipino",
                    "place_of_birth": birth_place,
                    "sex": gender,
                    "surname": surname,
                    "qrcode_svg_1": f"{identification_no};{given_name};{surname}",
                }
            }
            data_str = str(data).replace("'", '"')
            _logger.info("ID PASS Data: %s" % data_str)

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            response = requests.post(
                id_pass_param[0].api_url,
                headers=headers,
                data=data_str,
            )
            if response.status_code == 200:
                pdf_vals = response.json()
                file_pdf = pdf_vals["files"]["pdf"]
                file_pdf = file_pdf[28:]
                self.id_pdf = file_pdf
                self.id_pdf_filename = (
                    id_pass_param[0].filename_prefix
                    + full_name.strip()
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
                "ID PASS Response: %s Code: %s"
                % (response.reason, response.status_code)
            )
            return
        else:
            raise ValidationError(_("ID Pass Error: No API set"))  # noqa: C901
