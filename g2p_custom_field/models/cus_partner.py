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


import json
import logging

from lxml import etree

from odoo import models

_logger = logging.getLogger(__name__)


class G2PResPartner(models.Model):
    _inherit = "res.partner"

    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super(G2PResPartner, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )

        if view_type == "form":
            doc = etree.XML(res["arch"])
            basic_info_page = doc.xpath("//page[@name='basic_info']")

            model_fields_id = self.env["ir.model.fields"].search(
                [("model_id", "=", "res.partner")],
                order="ttype, field_description",
            )

            if basic_info_page:
                is_group = self._context.get("default_is_group", False)
                custom_page = etree.Element("page", {"string": "Addtional Details"})
                criteria_page = etree.Element("page", {"string": "Criteria"})

                custom_group = etree.SubElement(
                    custom_page, "group", {"col": "4", "colspan": "4"}
                )
                criteria_group = etree.SubElement(
                    criteria_page, "group", {"col": "4", "colspan": "4"}
                )

                for rec in model_fields_id:
                    els = rec.name.split("_")
                    if len(els) >= 3 and (
                        els[2] == "grp" and not is_group or els[2] == "ind" and is_group
                    ):
                        continue
                    if len(els) >= 2 and els[1] == "cst":
                        etree.SubElement(custom_group, "field", {"name": rec.name})
                    elif len(els) >= 2 and els[1] == "crt":
                        new_field = etree.SubElement(
                            criteria_group,
                            "field",
                            {
                                "name": rec.name,
                                "readonly": "1",
                                "class": "oe_read_only",
                            },
                        )
                        new_field.set("readonly", "1")
                        modifiers = {"readonly": True}
                        new_field.set("modifiers", json.dumps(modifiers))

                if custom_group.getchildren():
                    basic_info_page[0].addnext(custom_page)
                if criteria_group.getchildren():
                    basic_info_page[0].addnext(criteria_page)

                res["arch"] = etree.tostring(doc, encoding="unicode")

        return res
