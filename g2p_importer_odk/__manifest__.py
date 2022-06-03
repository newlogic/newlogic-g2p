# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.

{
    "name": "G2P ODK Importer",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 3,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "LGPL-3",
    "depends": [
        "base",
        "g2p_additional_data",
        # "g2p_location",
        "g2p_registrant",
        # oca
        "connector_importer",
    ],
    "data": [
        "views/source_views.xml",
        "security/ir.model.access.csv",
        "data/import_backend.xml",
        "data/import_type.xml",
        "data/import_source.xml",
        "data/import_recordset.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
