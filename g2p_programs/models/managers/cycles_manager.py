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


class BaseCyclesManager(models.AbstractModel):
    _name = "g2p.cycles.manager"

    program_id = fields.Many2one("g2p.program", string="Program", editable=False)

    def last_cycle(self):
        """
        Returns the last cycle of the program
        Returns:
            cycle: the last cycle of the program
        """
        # TODO: implement this
        raise NotImplementedError()

    def new_cycle(self):
        """
        Create the next cycle of the program
        Returns:
            cycle: the newly created cycle
        """
        raise NotImplementedError()

    def active_cycle(self):
        """
        Returns the active cycle of the program
        Returns:
            cycle: the active cycle of the program
        """
        # TODO: implement this
        raise NotImplementedError()

    def activate_cycle(self, cycle):
        """
        Activate the cycle
        Args:
            cycle: the cycle to activate
        """
        # TODO: implement this; deactivate the others
        raise NotImplementedError()


class SimpleCycleManager(models.Model):
    _name = "g2p.cycles.manager.simple"
    _inherit = "g2p.cycles.manager"

    number_of_cycles = fields.Integer(string="Number of cycles", default=1)

    #  TODO: review 'calendar.recurrence' module, it seem the way to go for managing the recurrence
    # recurrence_id = fields.Many2one('calendar.recurrence', related='event_id.recurrence_id')

    def new_cycle(self):
        #  TODO: implement this and set the start date of the new cycle based on the last cycle and the recurrence.
        pass
