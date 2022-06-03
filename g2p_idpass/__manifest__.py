# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.


{
    "name": "ID PASS Module",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "LGPL-3",
    "depends": ["base", "g2p_registrant"],
    "data": [
        "data/id_pass.xml",
        "views/registrant.xml",
        "security/ir.model.access.csv",
        "views/id_pass_view.xml",
    ],
    "assets": {},
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
