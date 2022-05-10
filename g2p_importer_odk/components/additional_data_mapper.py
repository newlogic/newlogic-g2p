from odoo.addons.component.core import Component


class ProductProductMapper(Component):
    _name = "g2p.additional.data.mapper"
    _inherit = "importer.base.mapper"
    _apply_on = "g2p.additional.data"

    # TODO: How do we set source_id and tag_ids?
    direct = [
        # in direct mapping here:
        # https://github.com/OCA/connector/blob/13.0/connector/components/mapper.py#L891
        ("id", "id"),
        ("name", "name"),
        ("json", "json"),
    ]
