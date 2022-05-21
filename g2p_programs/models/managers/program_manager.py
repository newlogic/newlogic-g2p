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
from datetime import datetime

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ProgramManager(models.Model):
    _name = "g2p.program.manager"
    _description = "Program Manager"
    _inherit = "g2p.manager.mixin"

    program_id = fields.Many2one("g2p.program", "Program")

    @api.model
    def _selection_manager_ref_id(self):
        selection = super()._selection_manager_ref_id()
        new_manager = ("g2p.program.manager.default", "Default")
        if new_manager not in selection:
            selection.append(new_manager)
        return selection


class BaseProgramManager(models.AbstractModel):
    _name = "g2p.base.program.manager"
    _description = "Base Program Manager"

    name = fields.Char("Manager Name", required=True)
    program_id = fields.Many2one("g2p.program", string="Program", required=True)

    def last_cycle(self):
        """
        Returns the last cycle of the program
        Returns:
            cycle: the last cycle of the program
        """
        # TODO: implement this
        # sort the program's cycle by sequence and return the last one
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


class DefaultProgramManager(models.Model):
    _name = "g2p.program.manager.default"
    _inherit = ["g2p.base.program.manager", "g2p.manager.source.mixin"]
    _description = "Default Program Manager"

    number_of_cycles = fields.Integer(string="Number of cycles", default=1)
    copy_last_cycle_on_new_cycle = fields.Boolean(
        string="Copy previous cycle", default=True
    )

    #  TODO: review 'calendar.recurrence' module, it seem the way to go for managing the recurrence
    # recurrence_id = fields.Many2one('calendar.recurrence', related='event_id.recurrence_id')

    def new_cycle(self):
        """
        Create the next cycle of the program
        Returns:
            cycle: the newly created cycle
        """
        for rec in self:
            cycles = self.env["g2p.cycle"].search([("program_id", "=", rec.program_id.id)])
            new_cycle = None
            _logger.info("cycles: %s", cycles)
            if len(cycles) == 0:
                if rec.program_id.cycle_managers:
                    _logger.info("cycle managers: %s", rec.program_id.cycle_managers)
                    rec.program_id.cycle_managers.ensure_one()
                    for cm in rec.program_id.cycle_managers:
                        new_cycle = cm.manager_ref_id.new_cycle("Cycle 1", datetime.now())
            return new_cycle
