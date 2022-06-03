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
{
    "name": "G2P Programs",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "Other OSI approved licence",
    "depends": [
        "base",
        "mail",
        "sms",
        "queue_job",
        "g2p_registrant",
        "account",
        "l10n_generic_coa",
    ],
    "data": [
        "security/program_security.xml",
        "security/ir.model.access.csv",
        "data/sequences.xml",
        "report/voucher_card.xml",
        "report/report_format.xml",
        "views/main_view.xml",
        "views/programs_view.xml",
        "views/program_membership_view.xml",
        "views/cycle_view.xml",
        "views/cycle_membership_view.xml",
        "views/voucher_view.xml",
        "views/registrant_view.xml",
        "views/managers/eligibility_manager_view.xml",
        "views/managers/deduplication_manager_view.xml",
        "views/managers/notification_manager_view.xml",
        "views/managers/program_manager_view.xml",
        "views/managers/cycle_manager_view.xml",
        "views/managers/entitlement_manager_view.xml",
        "views/accounting/fund_management_view.xml",
        "views/accounting/account_journal_view.xml",
        "views/accounting/fund_report_view.xml",
        "views/accounting/account_journal_config_view.xml",
        "wizard/assign_to_program_wizard.xml",
    ],
    "assets": {},
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
