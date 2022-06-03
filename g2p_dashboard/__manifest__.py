# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
{
    "name": "G2P Dashboard",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "LGPL-3",
    "depends": ["base", "g2p_registrant", "g2p_programs", "odoo_dynamic_dashboard"],
    "data": [
        "views/main_view.xml",
        "views/dashboard_menu_view.xml",
        "views/programs_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "g2p_dashboard/static/src/js/dynamic_dashboard.js",
        ],
        "web.assets_qweb": [],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
