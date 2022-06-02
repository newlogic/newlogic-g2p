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
    "name": "G2P POS Module",
    "category": "G2P",
    "version": "15.0.0.0.1",
    "sequence": 1,
    "author": "Newlogic",
    "website": "https://newlogic.com/",
    "license": "Other OSI approved licence",
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
