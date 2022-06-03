# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.

import logging
from ast import literal_eval

from odoo import models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class DashBoardBlock(models.Model):
    _inherit = "dashboard.block"

    def get_dashboard_vals(self, action_id, active_id):
        """Dashboard block values"""
        block_id = []
        dashboard_block = (
            self.env["dashboard.block"]
            .sudo()
            .search([("client_action", "=", int(action_id))])
        )
        for rec in dashboard_block:
            color = rec.tile_color if rec.tile_color else "#1f6abb;"
            icon_color = rec.tile_color if rec.tile_color else "#1f6abb;"
            text_color = rec.text_color if rec.text_color else "#FFFFFF;"
            vals = {
                "id": rec.id,
                "name": rec.name,
                "type": rec.type,
                "graph_type": rec.graph_type,
                "icon": rec.fa_icon,
                "cols": rec.graph_size,
                "color": "background-color: %s;" % color,
                "text_color": "color: %s;" % text_color,
                "icon_color": "color: %s;" % icon_color,
            }
            domain = []
            if rec.filter:
                domain = expression.AND([literal_eval(rec.filter)])
                idx1 = 0
                for dom in domain:
                    if type(dom) in (list, tuple):
                        if type(dom) == tuple:
                            dom = list(dom)
                        try:
                            idx2 = dom.index("active_id")
                        except Exception:
                            idx2 = None
                        if idx2:
                            # _logger.info("DEBUG! context: %s", self.env.context)
                            dom[idx2] = active_id
                        domain[idx1] = tuple(dom)
                    idx1 += 1
                _logger.info("DEBUG! domain: %s", domain)

            if rec.model_name:
                if rec.type == "graph":
                    query = self.env[rec.model_name].get_query(
                        domain, rec.operation, rec.measured_field, group_by=rec.group_by
                    )
                    self._cr.execute(query)
                    records = self._cr.dictfetchall()
                    print(query, "query")
                    print(records, "records")
                    x_axis = []
                    for record in records:
                        x_axis.append(record.get(rec.group_by.name))
                    y_axis = []
                    for record in records:
                        y_axis.append(record.get("value"))
                    vals.update({"x_axis": x_axis, "y_axis": y_axis})
                else:
                    query = self.env[rec.model_name].get_query(
                        domain, rec.operation, rec.measured_field
                    )
                    self._cr.execute(query)
                    records = self._cr.dictfetchall()
                    magnitude = 0
                    total = records[0].get("value")
                    while abs(total) >= 1000:
                        magnitude += 1
                        total /= 1000.0
                    # add more suffixes if you need them
                    val = "%.2f%s" % (total, ["", "K", "M", "G", "T", "P"][magnitude])

                    # if rec.measured_field.ttype == 'monetary':
                    # amount = str(
                    #     value) + currency_id.symbol if currency_id.position == 'after' else currency_id.symbol + str(
                    #     value)
                    records[0]["value"] = val
                    vals.update(records[0])
            block_id.append(vals)
        print(block_id, "dhressssssssssss")
        return block_id
