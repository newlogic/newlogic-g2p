# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class ResPartnerGroupMapper(Component):
    _name = "g2p.res.partner.group.data.mapper"
    _inherit = "importer.base.mapper"
    _apply_on = "res.partner"

    # TODO: How do we set tag_ids?
    direct = [
        ("id", "id"),
        ("name", "name"),
        ("given_name", "given_name"),
        ("family_name", "family_name"),
        ("gender", "gender"),
        ("birthdate", "birthdate"),
        ("addl_name", "addl_name"),
        # ("birth_place", "birth_place"),
        # ("registration_date", "registration_date"),
        ("is_registrant", "is_registrant"),
        ("is_group", "is_group"),
    ]

    _logger.debug(f"ResultMap: {direct}")
