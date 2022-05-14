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
from odoo import _, exceptions, fields, models
from odoo.tools import safe_eval

from odoo.addons.queue_job.job import DONE


class BaseManager(models.AbstractModel):
    _name = "base.programs.manager"

    def _get_eval_context(self):
        """Prepare the context used when evaluating python code
        :returns: dict -- evaluation context given to safe_eval
        """
        return {
            "datetime": safe_eval.datetime,
            "dateutil": safe_eval.dateutil,
            "time": safe_eval.time,
            "uid": self.env.uid,
            "user": self.env.user,
        }

    def _safe_eval(self, string, locals_dict=None):
        """Evaluates a string containing a Python expression.
        :param string: string expression to be evaluated
        :param locals_dict: local variables for evaluation
        :returns: the result of the evaluation
        """
        return safe_eval(string, self._get_eval_context(), locals_dict)


class JobRelatedMixin(models.AbstractModel):
    """Mixin klass for queue.job relationship.

    Note that we support only 1 job at a time.
    If we want to support Queued Jobs, `queue.job.batch` will be needed.
    """

    _name = "g2p.job.mixin"

    job_id = fields.Many2one("queue.job", string="Job", readonly=True)
    job_state = fields.Selection(index=True, related="job_id.state")
    job_type = fields.Char("Job Type", readonly=True)

    def has_job(self):
        return bool(self.job_id)

    def job_done(self):
        return self.job_state == DONE

    def can_create_new_job(self):
        if self.has_job() and not self.job_done():
            return False
        return True

    def _check_delete(self):
        if self.has_job() and not self.job_done():
            raise exceptions.Warning(_("You must complete the job first!"))

    def unlink(self):
        for item in self:
            item._check_delete()
        return super().unlink()
