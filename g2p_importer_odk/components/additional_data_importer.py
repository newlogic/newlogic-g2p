# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
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
            "json": json.dumps(res),
            "_line_nr": -1,
        }
        return new_res
