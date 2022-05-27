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

from odoo.addons.component.core import Component

# from ..log import logger

_logger = logging.getLogger(__name__)


class G2PResPartnerGroupDataRecordImporter(Component):
    _name = "g2p.res.partner.group.data.importer"
    _inherit = ["importer.record"]
    _apply_on = "res.partner"
    odoo_unique_key = "id"
    odoo_unique_key_is_xmlid = True

    def is_group(self, g2p_type):
        if g2p_type == "individual":
            return False

        return True

    def full_name(self, first, last, addl):
        name = str(last.upper()) + ", " + str(first.upper()) + " " + str(addl.upper())

        return name

    def prepare_line_data(
        self,
        id,
        name=None,
        given_name=None,
        family_name=None,
        gender=None,
        birthdate=None,
        addl_name=None,
        membership_type=None,
        is_group=False,
    ):
        if is_group:
            data = {
                "id": id,
                "name": name,
                "is_registrant": "True",
                "is_group": is_group,
                "_line_nr": -1,
            }
        else:
            fullname = self.full_name(given_name, family_name, addl_name)
            _logger.debug(f"Fullname: {fullname}")
            data = {
                "id": id,
                "name": fullname,
                "given_name": given_name,
                "family_name": family_name,
                "gender": gender,
                "birthdate": birthdate,
                "addl_name": addl_name,
                "membership_type": membership_type,
                "is_registrant": True,
                "is_group": is_group,
                "_line_nr": -1,
            }

        return data

    def prepare_line(self, line):
        res = super().prepare_line(line)
        odk_id = res["__id"].split(":")[1]
        group_id = f"odk.group.{odk_id}"
        group_name = f'{res["__g2p_kind__"]}-{odk_id}'
        is_group = self.is_group(res["__g2p_type__"])

        new_res = self.prepare_line_data(
            id=group_id,
            name=group_name,
            is_group=is_group,
        )

        return new_res

    def prepare_line_extension(self, res):
        odk_id = res["__id"].split(":")[1]
        # is_group = self.is_group(res['__g2p_type__'])

        members_list = []
        for member in res:
            if member == "principal_recipient":
                principal_id = f"odk.individual.{odk_id}"
                is_group = self.is_group(res[member]["__g2p_type__"])
                gender = str(res[member]["sex"]).capitalize()

                data = self.prepare_line_data(
                    id=principal_id,
                    given_name=res[member]["first_name"],
                    family_name=res[member]["last_name"],
                    gender=gender,
                    birthdate=res[member]["date_of_birth"],
                    addl_name=res[member]["patronymic_name"],
                    membership_type=res[member]["__g2p_membership_type__"],
                    is_group=is_group,
                )

                members_list.append(data)

            if member == "other_adults":
                for adult in res["other_adults"]:
                    is_group = self.is_group(adult["__g2p_type__"])
                    adult_id = f"odk.individual.{adult['__id']}"
                    adult_gender = str(adult["sex"]).capitalize()

                    data = self.prepare_line_data(
                        id=adult_id,
                        given_name=adult["first_name"],
                        family_name=adult["last_name"],
                        gender=adult_gender,
                        birthdate=adult["date_of_birth"],
                        addl_name=adult["patronymic_name"],
                        is_group=is_group,
                    )

                    members_list.append(data)

            if member == "other_children":
                for children in res["other_children"]:
                    is_group = self.is_group(children["__g2p_type__"])
                    children_id = f"odk.individual.{children['__id']}"
                    children_gender = str(children["sex"]).capitalize()

                    data = self.prepare_line_data(
                        id=children_id,
                        given_name=children["first_name"],
                        family_name=children["last_name"],
                        gender=children_gender,
                        birthdate=children["date_of_birth"],
                        addl_name=children["patronymic_name"],
                        is_group=is_group,
                    )
                    members_list.append(data)

        return members_list

    def run(self, record, is_last_importer=True, **kw):
        res = super(G2PResPartnerGroupDataRecordImporter, self).run(
            record, is_last_importer=True, **kw
        )

        for line in self._record_lines():
            lines = self.prepare_line_extension(line)
            options = self._load_mapper_options()

            prepare_line = self.prepare_line(line)
            group_id = self.env.ref(f"{prepare_line['id']}").id

            odoo_record = None
            _logger.debug(f"Result_lines: {lines}")
            _logger.debug(f"Result_lines: {len(lines)}")

            for ln in lines:
                # _logger.debug(f"Odoo_Created: {ln}")
                membership_type = ln["membership_type"]
                kinds = []
                if membership_type:
                    m_types = membership_type.split(",")
                    _logger.debug(f"Odoo_Created: {m_types}")
                    for m_type in m_types:
                        if m_type == "Head of household":
                            kinds.append(
                                self.env.ref(
                                    "g2p_registrant.group_membership_kind_head_household"
                                ).id
                            )
                        elif m_type == "Principal recipient":
                            kinds.append(
                                self.env.ref(
                                    "g2p_registrant.group_membership_kind_principal_recipient"
                                ).id
                            )

                _logger.debug(f"kinds: {kinds}")
                try:
                    with self.env.cr.savepoint():
                        values = self.mapper.map_record(ln).values(**options)

                except Exception as err:
                    values = {}
                    self.tracker.log_error(values, ln, odoo_record, message=err)
                    if self._break_on_error:
                        raise
                    continue

                # handle forced skipping
                skip_info = self.skip_it(values, ln)
                if skip_info:
                    self.tracker.log_skipped(values, ln, skip_info)
                    continue

                try:
                    with self.env.cr.savepoint():
                        if self.record_handler.odoo_exists(values, ln):
                            odoo_record = self.record_handler.odoo_write(values, ln)
                            self.tracker.log_updated(values, ln, odoo_record)
                        else:
                            if self.work.options.importer.write_only:
                                self.tracker.log_skipped(
                                    values,
                                    ln,
                                    {
                                        "message": "Write-only importer, record not found."
                                    },
                                )
                                continue
                            odoo_record = self.record_handler.odoo_create(values, ln)
                            self.tracker.log_created(values, ln, odoo_record)

                            self.env["g2p.group.membership"].create(
                                {
                                    "group": group_id,
                                    "individual": odoo_record[0].id,
                                    "kind": [(4, kind) for kind in kinds],
                                }
                            )

                except Exception as err:
                    self.tracker.log_error(values, ln, odoo_record, message=err)
                    if self._break_on_error:
                        raise
                    continue
        return res
