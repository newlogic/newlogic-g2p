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


class CycleDashBoard(models.Model):
    _inherit = "g2p.cycle"

    @api.model
    def count_cycles(self, state=None):
        """
        Get total cycles per status
        """
        domain = []
        if state is not None:
            domain = [
                ("state", "in", state),
                ("company_id", "=", self.env.user.company_id.id),
            ]

        total = self.search_count(domain)
        return {"value": total}

    @api.model
    def get_cycle_ids(self, state=None):
        """
        Get ids of all cycles by state
        """
        domain = []
        if state:
            domain = [("state", "in", state)]
        return self.search(domain).ids or None
