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
from odoo.addons.component.core import Component
from odoo.addons.connector_importer.utils.mapper_utils import xmlid_to_rel


class ProductProductMapper(Component):
    _name = "g2p.additional.data.mapper"
    _inherit = "importer.base.mapper"
    _apply_on = "g2p.additional.data"

    # TODO: How do we set tag_ids?
    direct = [
        ("id", "id"),
        ("name", "name"),
        ("json", "json"),
        (xmlid_to_rel("source_id"), "source_id"),
    ]
