# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.


{
    "name": "G2P Additional Data Module",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "LGPL-3",
    "depends": ["base", "g2p_registrant"],
    "data": [
        "security/ir.model.access.csv",
        "views/additional_data.xml",
        "views/additional_data_tags.xml",
        "views/datasource.xml",
        "views/registrant_additional_data.xml",
        # "views/individual_views.xml",
        # "views/group_views.xml",
    ],
    "assets": {},
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
