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

        doc = etree.XML(res["arch"])

        if view_type == "form":
            doc = etree.XML(res["arch"])
            other_page = doc.xpath("//page[@name='other']")

            model_fields_id = self.env["ir.model.fields"].search(
                [("model_id", "=", "res.partner"), ("state", "=", "manual")]
            )

            if other_page:
                custom_page = etree.Element("page", {"string": "Custom Fields"})
                criteria_page = etree.Element("page", {"string": "Criteria Fields"})
                other_page[0].addprevious(custom_page)
                other_page[0].addprevious(criteria_page)

                custom_group = etree.SubElement(
                    custom_page, "group", {"col": "4", "colspan": "4"}
                )
                criteria_group = etree.SubElement(
                    criteria_page, "group", {"col": "4", "colspan": "4"}
                )

                for rec in model_fields_id:
                    if rec.name.startswith("x_custom_"):
                        etree.SubElement(
                            custom_group,
                            "field",
                            {
                                "name": f"{rec.name}",
                            },
                        )

                    if rec.name.startswith("x_criteria_"):
                        # doc.xpath("//page[@name='other']")
                        etree.SubElement(
                            criteria_group,
                            "field",
                            {
                                "name": f"{rec.name}",
                                "readonly": "1",
                            },
                        )

                res["arch"] = etree.tostring(doc, encoding="unicode")

        return res
