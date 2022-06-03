# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
{
    "name": "G2P Program Dashboard",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "LGPL-3",
    "depends": ["base", "g2p_registrant", "g2p_programs"],
    "data": [
        "views/dashboard_views.xml",
        "views/programs_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "g2p_program_dashboard/static/src/scss/style.scss",
            "g2p_program_dashboard/static/libs/bootstrap-toggle-master/css/bootstrap-toggle.min.css",
            "g2p_program_dashboard/static/src/js/program_dashboard.js",
            "g2p_program_dashboard/static/src/js/dashboard_form_widget.js",
            "g2p_program_dashboard/static/libs/Chart.bundle.js",
            "g2p_program_dashboard/static/libs/Chart.bundle.min.js",
            "g2p_program_dashboard/static/libs/Chart.min.js",
            "g2p_program_dashboard/static/libs/Chart.js",
            "g2p_program_dashboard/static/libs/bootstrap-toggle-master/js/bootstrap-toggle.min.js",
        ],
        "web.assets_qweb": [
            "g2p_program_dashboard/static/src/xml/dashboard_template.xml",
        ],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
