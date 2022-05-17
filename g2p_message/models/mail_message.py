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

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


# Used to render html field in TreeView
TREE_TEMPLATE = (
    '<table style="width:100%%;border:none;%s" title="%s">'
    "<tbody>"
    "<tr>"
    '<td style="width: 5%%;"><img class="rounded-circle"'
    ' style="width: 64px; padding:10px;" src="data:image/png;base64,%s"'
    ' alt="Avatar" title="%s" width="100" border="0" /></td>'
    '<td style="width: 99%%;">'
    '<table style="width: 100%%; border: none;">'
    "<tbody>"
    "<tr>"
    '<td id="author"><strong>"%s"</strong> &nbsp; <span id="subject">%s</span></td>'
    '<td id="date" style="text-align:right;"><span title="%s" id="date">%s</span></td>'
    "</tr>"
    "<tr>"
    "<td>"
    '<td style="text-align: right;">%s</td>'
    "</tr>"
    "</tbody>"
    "</table>"
    "<tr><td>"
    '<p id="text-preview" style="color: #808080;">%s</p>'
    "</td>"
    "</tr>"
    "</td>"
    "</tr>"
    "</tbody>"
    "</table>"
)


class G2PMailMessage(models.Model):
    _inherit = "mail.message"

    subject_display = fields.Html(
        string="Subject Display", compute="_compute_subject_display"
    )
    subtype_description = fields.Text(
        string="Subtype Description", related="subtype_id.description"
    )
    track_display = fields.Html(
        string="Track Display", compute="_compute_track_display"
    )
    source_id = fields.Char(string="Source", compute="_compute_source_id")

    @api.depends("model")
    def _compute_source_id(self):
        for rec in self:
            source = self.env[f"{rec.model}"].browse(rec.res_id)
            if source:
                rec.source_id = source.display_name
            else:
                rec.source_id = "No Model"

    def source_name(self):
        context = self._context.copy()
        return {
            "name": "form_name",
            "view_type": "form",
            "view_mode": "form",
            "res_model": f"{self.model}",
            "type": "ir.actions.act_window",
            "res_id": self.res_id,
            "target": "main",
            "context": context,
        }

    @api.depends("tracking_value_ids.field")
    def _compute_track_display(self):
        for rec in self:
            html = """\
                <table>
                """
            for track_val in rec.tracking_value_ids:
                html = html + "<tr>"
                html = (
                    html + "<td>" + str(track_val.field.field_description) + ": &nbsp;"
                )
                if track_val.field.ttype == "char":
                    html += (
                        (
                            str(track_val.old_value_char)
                            if track_val.old_value_char
                            else ""
                        )
                        + "&nbsp; &rarr; &nbsp;"
                        + str(track_val.new_value_char)
                        + "</td>"
                    )
                if track_val.field.ttype == "date":
                    html += (
                        (
                            str(track_val.old_value_datetime.strftime("%m/%d/%y"))
                            if track_val.old_value_datetime
                            else ""
                        )
                        + "&nbsp; &rarr; &nbsp;"
                        + str(track_val.new_value_datetime.strftime("%m/%d/%y"))
                        + "</td>"
                    )
                if track_val.field.ttype == "datetime":
                    html += (
                        (
                            str(
                                track_val.old_value_datetime.strftime(
                                    "%m/%d/%y %H:%M:%S"
                                )
                            )
                            if track_val.old_value_datetime
                            else ""
                        )
                        + "&nbsp; &rarr; &nbsp;"
                        + str(
                            track_val.new_value_datetime.strftime("%m/%d/%y %H:%M:%S")
                        )
                        + "</td>"
                    )
                if track_val.field.ttype == "selection":
                    html += (
                        (
                            str(track_val.old_value_char)
                            if track_val.old_value_char
                            else ""
                        )
                        + "&nbsp; &rarr; &nbsp;"
                        + str(track_val.new_value_char)
                        + "</td>"
                    )
                if track_val.field.ttype == "boolean":
                    old_bool_val = ""
                    new_bool_val = ""
                    if track_val.old_value_integer:
                        old_bool_val = "True"
                    else:
                        old_bool_val = "False"

                    if track_val.new_value_integer:
                        new_bool_val = "True"
                    else:
                        new_bool_val = "False"

                    html += (
                        (str(old_bool_val))
                        + "&nbsp; &rarr; &nbsp;"
                        + str(new_bool_val)
                        + "</td>"
                    )
                if track_val.field.ttype == "float":
                    html += (
                        (
                            str(track_val.old_value_float)
                            if track_val.old_value_float
                            else ""
                        )
                        + "&nbsp; &rarr; &nbsp;"
                        + str(track_val.new_value_float)
                        + "</td>"
                    )
                if track_val.field.ttype == "integer":
                    html += (
                        (
                            str(track_val.old_value_integer)
                            if track_val.old_value_integer
                            else ""
                        )
                        + "&nbsp; &rarr; &nbsp;"
                        + str(track_val.new_value_integer)
                        + "</td>"
                    )
                if track_val.field.ttype == "monetary":
                    html += (
                        (
                            str(track_val.old_value_monetary)
                            if track_val.old_value_monetary
                            else ""
                        )
                        + "&nbsp; &rarr; &nbsp;"
                        + str(track_val.new_value_monetary)
                        + "</td>"
                    )

                html = html + "</tr>"
            html = html + "</table>"

            rec.track_display = html

    # -- Get Subject for tree view
    @api.depends("subject")
    def _compute_subject_display(self):
        for rec in self.with_context(bin_size=False):
            # Compose notification icons
            notification_icons = ""
            if rec.starred:
                notification_icons = (
                    '%s &nbsp;<i class="fa fa-star" title="%s"></i>'
                    % (notification_icons, _("Starred"))
                )

            # Compose preview body
            rec.subject_display = TREE_TEMPLATE % (
                ("background-color: white;"),
                rec.author_id.name,
                rec.author_avatar.decode("utf-8"),
                rec.author_id.name,
                rec.author_id.name,
                rec.subject if rec.subject else "",
                rec.date,
                rec.date,
                # notification_icons,
                rec.source_id,
                # create computed value of tracking values to get track value note
                rec.body
                if rec.body
                else (
                    rec.subtype_id.description
                    if rec.subtype_id.description
                    else (rec.track_display if rec.track_display else "")
                ),
                # rec.description if rec.description
                # else rec.subtype_id.description,
            )
