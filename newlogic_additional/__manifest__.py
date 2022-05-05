# -*- coding: utf-8 -*-
#################################################################################
# Author      : Newlogic (<https://newlogic.com/>)
# Copyright(c): Newlogic
# All Rights Reserved.
#################################################################################
{
  "name"         :  "Newlogic Additional Data Object",
  "category"     :  "NewLogic",
  "version"      :  "0.0.1",
  "sequence"     :  1,
  "author"       :  "Newlogic",
  "website"      :  "https://newlogic.com/",
  "license"      :  "LGPL-3",
  "description"  :  """
  Newlogic Additional Data Object
  ========================

  - 
  
  """,
  "depends"      :  ['base', 'newlogic_main'],
  "data"         :  [
                     'security/ir.model.access.csv',
                     'views/additional_data.xml',
                     'views/additional_data_tags.xml',
                     'views/datasource.xml',
                     'views/registrant_additional_data.xml',
                    ],
  'assets'       :  {},
  "demo"         :  [],
  "images"       :  [],
  "application"  :  True,
  "installable"  :  True,
  "auto_install" :  False,
}
