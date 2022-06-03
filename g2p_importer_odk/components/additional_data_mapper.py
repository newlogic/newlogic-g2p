# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
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
