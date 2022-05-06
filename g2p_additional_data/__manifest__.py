# -*- coding: utf-8 -*-
#################################################################################
# Author      : Newlogic (<https://newlogic.com/>)
# Copyright(c): Newlogic
# All Rights Reserved.
#################################################################################
{
  "name"         :  "Newlogic Additional Data Module",
  "category"     :  "G2P",
  "version"      :  "0.0.1",
  "sequence"     :  1,
  "author"       :  "Newlogic",
  "website"      :  "https://newlogic.com/",
  "license"      :  "Apache 2.0",
  "description"  :  """
  Newlogic Additional Data
  ========================

  - 
  
  """,
  "depends"      :  ['base', 'g2p_registrant'],
  "data"         :  [
                     'security/ir.model.access.csv',
                     'views/additional_data.xml',
                     'views/additional_data_tags.xml',
                     'views/datasource.xml',
                     'views/registrant_additional_data.xml',
                     'views/registrant_views.xml',
                    ],
  'assets'       :  {},
  "demo"         :  [],
  "images"       :  [],
  "application"  :  True,
  "installable"  :  True,
  "auto_install" :  False,
}
