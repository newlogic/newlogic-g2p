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

from odoo import fields, models, tools, _

class ProgramFundReport(models.Model):
    _name = "g2p.program.fund.report.view"
    _description = "Program Fund Report"
    _auto = False
    _table = "g2p_program_fund_report_view"

    name = fields.Char("Source Document", readonly=True)
    partner_id = fields.Many2one("res.partner", "Beneficiary", readonly=True)
    company_id = fields.Many2one("res.company", readonly=True)
    program_id = fields.Many2one("g2p.program", "Program", readonly=True)
    journal_id = fields.Many2one("account.journal","Accounting Journal",readonly=True)
    date_posted = fields.Date('Date',readonly=True)
    amount = fields.Monetary(required=True, currency_field="currency_id", readonly=True)
    currency_id = fields.Many2one("res.currency",readonly=True)

    def _select(self):
        select_str = """
            WITH trans AS (
                SELECT a.name as name,
                    NULL as partner_id,
                    a.company_id as company_id,
                    a.program_id as program_id,
                    a.journal_id as journal_id,
                    a.date_posted as date_posted,
                    a.amount as amount,
                    a.currency_id as currency_id
                FROM g2p_program_fund a
                WHERE a.state = 'posted'

                UNION ALL

                SELECT b.code as name,
                    b.partner_id as partner_id,
                    b.company_id as company_id,
                    d.id as program_id,
                    b.journal_id as journal_id,
                    f.date as date_posted,
                    e.amount * -1 as amount,
                    e.currency_id as currency_id
                FROM g2p_voucher b
                    LEFT JOIN g2p_cycle c on c.id = b.cycle_id
                        LEFT JOIN g2p_program d on d.id = c.program_id
                    LEFT JOIN account_payment e on e.id = b.disbursement_id
                        LEFT JOIN account_move f on f.id = e.move_id
                WHERE b.disbursement_id IS NOT NULL and e.payment_type = 'outbound'
            )
            
            SELECT 
                ROW_NUMBER () OVER (
                    ORDER BY date_posted) as id,
                name,
                partner_id,
                company_id,
                program_id,
                journal_id,
                date_posted,
                amount,
                currency_id
            FROM trans
            ORDER BY date_posted
        """
        return select_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            )""" % (self._table, self._select() ))
