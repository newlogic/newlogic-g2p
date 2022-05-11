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
# limitations under the License.#
import json

from odoo.addons.component.core import Component


class G2PAdditionalDataRecordImporter(Component):
    _name = "g2p.additional.data.importer"
    _inherit = ["importer.record"]
    _apply_on = "g2p.additional.data"
    odoo_unique_key = "id"
    odoo_unique_key_is_xmlid = True

    def prepare_line(self, line):
        res = super().prepare_line(line)
        odk_id = res["__id"].split(":")[1]
        new_res = {
            "id": f"odk.{odk_id}",
            "name": odk_id,
            "registered_on": res["start"],
            "source_id": res["source_id"],
            "location_id": res["location_id"],
            "json": json.dumps(res),
            "_line_nr": -1,
        }
        return new_res
