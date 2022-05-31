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


from odoo import api, models

# from odoo.http import request


class VoucherDashBoard(models.Model):
    _inherit = "g2p.voucher"

    @api.model
    def count_vouchers(self, state=None):
        """
        Get total vouchers per status
        """
        domain = [("company_id", "=", self.env.user.company_id.id)]
        if state is not None:
            domain += [("state", "in", state)]

        total = self.search_count(domain)
        return {"value": total}

    @api.model
    def get_voucher_ids(self, state=None):
        """
        Get ids of all vouchers by state
        """
        domain = [("company_id", "=", self.env.user.company_id.id)]
        if state:
            domain += [("state", "in", state)]
        return self.search(domain).ids or None

    @api.model
    def get_vouchers_month(self, *post):

        company_id = self.env.user.company_id and self.env.user.company_id.id or None
        params = (company_id,)

        sql = """select sum(initial_amount) as vouchers from g2p_voucher
                where company_id = %s AND state != 'cancelled'
                AND Extract(month FROM create_date::DATE) = Extract(month FROM DATE(NOW()))
                AND Extract(YEAR FROM create_date::DATE) = Extract(YEAR FROM DATE(NOW()))
            """
        self._cr.execute(sql, params)
        record_voucher_current_month = self._cr.dictfetchall()

        sql = """select sum(initial_amount) as vouchers_paid from g2p_voucher
                where company_id = %s AND state = 'approved'
                AND Extract(month FROM
                    case when date_approved is not null then
                        date_approved
                    else
                        write_date::DATE
                    end) = Extract(month FROM DATE(NOW()))
                AND Extract(YEAR FROM
                    case when date_approved is not null then
                        date_approved
                    else
                        write_date::DATE
                    end) = Extract(YEAR FROM DATE(NOW()))
            """
        self._cr.execute(sql, params)
        record_paid_voucher_current_month = self._cr.dictfetchall()

        total_voucher_current_month = [
            item["vouchers"] for item in record_voucher_current_month
        ]
        total_voucher_paid_current_month = [
            item["vouchers_paid"] for item in record_paid_voucher_current_month
        ]

        currency = self.get_currency(company_id)

        return (
            total_voucher_current_month,
            total_voucher_paid_current_month,
            currency,
        )

    @api.model
    def get_currency(self, company_id):
        current_company_id = company_id
        current_company = self.env["res.company"].browse(current_company_id)
        default = (
            current_company.currency_id or self.env.ref("base.main_company").currency_id
        )
        lang = self.env.user.lang
        if not lang:
            lang = "en_US"
        lang = lang.replace("_", "-")
        currency = {
            "position": default.position,
            "symbol": default.symbol,
            "language": lang,
        }
        return currency
