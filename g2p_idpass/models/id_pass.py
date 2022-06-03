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

from odoo import fields, models


class G2PIDPass(models.Model):
    _name = "g2p.id.pass"
    _description = "ID Pass"

    api_url = fields.Text("API URL")
    api_username = fields.Char("API Username")
    api_password = fields.Char("API Password")
    filename_prefix = fields.Char("File Name Prefix")
    expiry_length = fields.Integer("ID Expiry Length", default=1)
    expiry_length_type = fields.Selection(
        [("years", "Years"), ("months", "Months"), ("days", "Days")],
        "Length Type",
        default="years",
    )
    is_active = fields.Boolean("Active")
