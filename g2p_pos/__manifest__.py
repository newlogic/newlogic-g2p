# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
{
    "name": "G2P POS Module",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "LGPL-3",
    "depends": ["base", "point_of_sale", "g2p_registrant", "g2p_programs"],
    "assets": {
        "web.assets_backend": [
            "g2p_pos/static/src/js/action_button.js",
            "g2p_pos/static/src/js/popup_voucher.js",
        ],
        "web.assets_qweb": [
            "g2p_pos/static/src/view/action_button.xml",
            "g2p_pos/static/src/view/popup_voucher.xml",
        ],
    },
    "data": ["data/voucher_product.xml"],
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
