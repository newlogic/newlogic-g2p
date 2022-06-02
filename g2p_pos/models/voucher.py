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

from odoo import api, models

_logger = logging.getLogger(__name__)


class G2PVoucher(models.Model):
    _inherit = "g2p.voucher"

    @api.model
    def get_voucher_code(self, code):
        _logger.info("Code: %s", code["code"])
        data = self.env["g2p.voucher"].search([("code", "=", code["code"])])
        if data:
            voucher = {
                "code": data[0].code,
                "amount": data[0].initial_amount,
                "status": "Success",
            }
            return voucher
        else:
            voucher = {"code": 0, "amount": 0, "status": "QR Doesn't Exist"}
            return voucher
