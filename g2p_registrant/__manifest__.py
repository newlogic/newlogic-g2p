# -*- coding: utf-8 -*-
#################################################################################
#   Copyright 2022 Newlogic
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#################################################################################
{
  "name"         :  "G2P registrant Module",
  "category"     :  "G2P",
  "version"      :  "0.0.1",
  "sequence"     :  1,
  "author"       :  "Newlogic",
  "website"      :  "https://newlogic.com/",
  "license"      :  "Other OSI approved licence",
  "description"  :  """
  G2P registrant Module
  ========================

  - 
  
  """,
  "depends"      :  ['base','mail'],
  "data"         :  [
                  'security/newlogic_security.xml',
                  'security/ir.model.access.csv',
                  'data/group_membership_kinds.xml',
                  'wizard/disable_registrant_view.xml',
                  'views/main_view.xml',
                  #'views/all_registrants_view.xml',
                  'views/individuals_view.xml',
                  'views/groups_view.xml',
                  'views/registrant_attribute_view.xml',
                  'views/group_membership_view.xml',
                  'views/membership_kinds_view.xml',
                  'views/reg_relationship_view.xml',
                  'views/relationships_view.xml',
                  'views/reg_id_view.xml',
                  'views/id_types_view.xml',
                    ],
  'assets'       :  {},
  "demo"         :  [],
  "images"       :  [],
  "application"  :  True,
  "installable"  :  True,
  "auto_install" :  False,
}
