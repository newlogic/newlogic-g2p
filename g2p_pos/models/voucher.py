# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.

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
