#
# Copyright (c) 2022 Newlogic.
#
# This file is part of newlogic-g2p-erp.
# See https://github.com/newlogic/newlogic-g2p-erp/ for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
{
    "name": "G2P Program Dashboard",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "Other OSI approved licence",
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
