#################################################################################
# Author      : Newlogic (<https://newlogic.com/>)
# Copyright(c): Newlogic
# All Rights Reserved.
#################################################################################
{
    "name": "G2P Location Module",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "Other OSI approved licence",
    "depends": ["base", "g2p_registrant"],
    "external_dependencies": {
        "python": [
            "xlrd",
        ]
    },
    "data": [
        "security/ir.model.access.csv",
        "views/individual_views.xml",
        "views/group_views.xml",
        "views/location.xml",
        "views/location_import_views.xml",
    ],
    "assets": {},
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
