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
import calendar
import logging
from datetime import datetime

from odoo import api, models

_logger = logging.getLogger(__name__)

# from odoo.http import request


class ProgramDashBoard(models.Model):
    _inherit = "g2p.program"

    @api.model
    def count_programs(self, state=None):
        """
        Get total Programs per status
        """
        domain = [("company_id", "=", self.env.user.company_id.id)]
        if state is not None:
            domain += [("state", "in", state)]

        total = self.search_count(domain)
        return {"value": total}

    @api.model
    def count_beneficiaries(self, state=None):
        """
        Get total Beneficiaries
        """
        domain = [("company_id", "=", self.env.user.company_id.id)]
        if state is not None:
            domain += [("state", "in", state)]

        total = 0
        for rec in self.search([]):
            total += rec.program_membership_ids.search_count(domain)
        return {"value": total}

    @api.model
    def get_program_ids(self, state=None):
        """
        Get ids of all programs by state
        """
        domain = [("company_id", "=", self.env.user.company_id.id)]
        if state:
            domain += [("state", "in", state)]
        return self.search(domain).ids or None

    @api.model
    def get_programs_month(self, *post):

        company_id = self.env.user.company_id and self.env.user.company_id.id or None

        day_list = []
        now = datetime.now()
        day = calendar.monthrange(now.year, now.month)[1]
        for x in range(1, day + 1):
            day_list.append(x)

        # _logger.info("DEBUG! company_id: %s", company_id)

        # TODO: Add date_created in g2p.program
        sql = """select count(id) as programs_count ,cast(to_char(create_date::DATE, 'DD')as int)
                    as date from g2p_program
                    where  Extract(month FROM create_date::DATE) = Extract(month FROM DATE(NOW()))
                    AND Extract(YEAR FROM create_date::DATE) = Extract(YEAR FROM DATE(NOW()))
                    AND company_id = %s and state != 'archived'
                    group by date
        """
        params = (company_id,)
        self._cr.execute(sql, params)
        programs_count_rec = self._cr.dictfetchall()

        # TODO: Add date_approved in g2p.program
        sql = """select count(id) as approved_programs_count ,cast(to_char(write_date::DATE, 'DD')as int) \
                   as date from g2p_program \
                   where  Extract(month FROM write_date::DATE) = Extract(month FROM DATE(NOW())) \
                   AND Extract(YEAR FROM write_date::DATE) = Extract(YEAR FROM DATE(NOW())) \
                   AND company_id = %s and state = 'approved' \
                   group by date
        """
        self._cr.execute(sql, params)
        approved_programs_count_rec = self._cr.dictfetchall()

        records = []
        for date in day_list:
            last_month_prog = list(
                filter(lambda m: m["date"] == date, programs_count_rec)
            )
            last_month_appr = list(
                filter(lambda m: m["date"] == date, approved_programs_count_rec)
            )
            if not last_month_prog and not last_month_appr:
                records.append(
                    {
                        "date": date,
                        "programs": 0,
                        "approved": 0,
                    }
                )
            elif (not last_month_prog) and last_month_appr:
                last_month_appr[0].update(
                    {
                        "programs": 0,
                        "approved": -1 * last_month_appr[0]["approved_programs_count"]
                        if last_month_appr[0]["approved_programs_count"] < 1
                        else last_month_appr[0]["approved_programs_count"],
                    }
                )
                records.append(last_month_appr[0])
            elif (not last_month_appr) and last_month_prog:
                last_month_prog[0].update(
                    {
                        "approved": 0,
                        "programs": -1 * last_month_prog[0]["programs_count"]
                        if last_month_prog[0]["programs_count"] < 1
                        else last_month_prog[0]["programs_count"],
                    }
                )
                records.append(last_month_prog[0])
            else:
                last_month_prog[0].update(
                    {
                        "programs": -1 * last_month_prog[0]["programs_count"]
                        if last_month_prog[0]["programs_count"] < 1
                        else last_month_prog[0]["programs_count"],
                        "approved": -1 * last_month_appr[0]["approved_programs_count"]
                        if last_month_appr[0]["approved_programs_count"] < 1
                        else last_month_appr[0]["approved_programs_count"],
                    }
                )
                records.append(last_month_appr[0])
        programs = []
        approved = []
        date = []
        for rec in records:
            programs.append(rec["programs"])
            approved.append(rec["approved"])
            date.append(rec["date"])
        return {
            "programs": programs,
            "approved": approved,
            "date": date,
        }
