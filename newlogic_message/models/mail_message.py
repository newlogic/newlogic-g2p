# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError, Warning

import logging
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
    '<td id="notifications" style="text-align: right;">%s</td>'
    "</tr>"
    "</tbody>"
    "</table>"
    '<p id="text-preview" style="color: #808080;">%s</p>'
    "</td>"
    "</tr>"
    "</tbody>"
    "</table>"
)

class NLMailMessage(models.Model):
    _inherit = "mail.message"

    subject_display = fields.Html(string="Subject Display", compute="_compute_subject_display")
    subtype_description = fields.Text(string='Subtype Description', related='subtype_id.description')
    track_display = fields.Html(string="Track Display", compute="_compute_track_display")

    @api.depends("tracking_value_ids.field")
    def _compute_track_display(self):
        for rec in self:
            html = """\
                <table>
                """
            for track_val in rec.tracking_value_ids:
                html = html + "<tr>"
                html = html + "<td>" + str(track_val.field.field_description) + ': &nbsp;'
                if track_val.field.ttype == 'char':
                    html += (str(track_val.old_value_char) if track_val.old_value_char else '') + '&nbsp; &rarr; &nbsp;' + str(track_val.new_value_char) + "</td>"
                if track_val.field.ttype == 'date':
                    html += (str(track_val.old_value_datetime.strftime("%m/%d/%y")) if track_val.old_value_datetime else '') + \
                        '&nbsp; &rarr; &nbsp;' + str(track_val.new_value_datetime.strftime("%m/%d/%y")) + "</td>"
                if track_val.field.ttype == 'datetime':
                    html += (str(track_val.old_value_datetime.strftime("%m/%d/%y %H:%M:%S")) if track_val.old_value_datetime else '') + \
                        '&nbsp; &rarr; &nbsp;' + str(track_val.new_value_datetime.strftime("%m/%d/%y %H:%M:%S")) + "</td>"
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
                # rec.res_id,
                notification_icons,
                #create computed value of tracking values to get track value note
                rec.body if rec.body else (rec.subtype_id.description if rec.subtype_id.description else ''),
                # rec.description if rec.description
                # else rec.subtype_id.description,
            )
