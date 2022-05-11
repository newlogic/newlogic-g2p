# -*- coding: utf-8 -*-
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
# limitations under the License.#

{
  "name"         :  "G2P ODK Importer",
  "category"     :  "G2P",
  "version"      :  "0.0.1",
  "sequence"     :  3,
  "author"       :  "Newlogic",
  "website"      :  "https://newlogic.com/",
  "license"      :  "Other OSI approved licence",
  "description"  :  """
  ODK Importer
  ========================
  - 
  
  """,
  "depends"      :  [
                    'base',
                    'g2p_additional_data',
                    'g2p_location',
                     # oca
                     "connector_importer",
  ],
  "data"         :  [
                    'views/source_views.xml',
                    "security/ir.model.access.csv",
                    'data/import_backend.xml',
                    'data/import_type.xml',
                    'data/import_source.xml',
                    'data/import_recordset.xml',
  ],

  "application"  :  True,
  "installable"  :  True,
  "auto_install" :  False,
}