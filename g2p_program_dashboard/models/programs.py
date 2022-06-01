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
    def count_program_beneficiaries(self, state=None, res_id=None):
        """
        Get total Beneficiaries by program
        """
        total = 0
        if res_id:
            domain = [("id", "=", res_id)]

            for rec in self.search(domain):
                if state:
                    program_membership_ids = rec.program_membership_ids.filtered(
                        lambda a: a.state in state
                    )
                else:
                    program_membership_ids = rec.program_membership_ids
                total += len(program_membership_ids)
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

        params = (company_id,)
        sql = """select count(id) as programs_count ,cast(to_char(create_date::DATE, 'DD')as int)
                    as date from g2p_program
                    where company_id = %s and state != 'archived'
                    AND Extract(month FROM create_date::DATE) = Extract(month FROM DATE(NOW()))
                    AND Extract(YEAR FROM create_date::DATE) = Extract(YEAR FROM DATE(NOW()))
                    group by date
            """
        self._cr.execute(sql, params)
        programs_count_rec = self._cr.dictfetchall()

        # TODO: Add date_ended in g2p.program
        sql = """select count(id) as ended_programs_count ,cast(to_char(date_ended, 'DD')as int)
                    as date from g2p_program
                    where company_id = %s and state = 'ended'
                    AND Extract(month FROM
                        case when date_ended is not null then
                            date_ended
                        else
                            write_date::DATE
                        end) = Extract(month FROM DATE(NOW()))
                    AND Extract(YEAR FROM
                        case when date_ended is not null then
                            date_ended
                        else
                            write_date::DATE
                        end) = Extract(YEAR FROM DATE(NOW()))
                    group by date
            """
        self._cr.execute(sql, params)
        ended_programs_count_rec = self._cr.dictfetchall()

        records = []
        for date in day_list:
            last_month_prog = list(
                filter(lambda m: m["date"] == date, programs_count_rec)
            )
            last_month_endd = list(
                filter(lambda m: m["date"] == date, ended_programs_count_rec)
            )

            records.append(
                {
                    "date": date,
                    "programs": 0
                    if not last_month_prog
                    else last_month_prog[0]["programs_count"],
                    "ended": 0
                    if not last_month_endd
                    else last_month_endd[0]["ended_programs_count"],
                }
            )

        programs = []
        ended = []
        date = []
        for rec in records:
            programs.append(rec["programs"])
            ended.append(rec["ended"])
            date.append(rec["date"])
        return {
            "programs": programs,
            "ended": ended,
            "date": date,
        }
