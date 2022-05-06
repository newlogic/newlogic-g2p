# -*- coding: utf-8 -*-
#################################################################################
# Author      : Newlogic (<https://newlogic.com/>)
# Copyright(c): Newlogic
# All Rights Reserved.
#################################################################################
{
  "name"         :  "Newlogic Location Module",
  "category"     :  "NewLogic",
  "version"      :  "0.0.1",
  "sequence"     :  1,
  "author"       :  "New Logic",
  "website"      :  "https://newlogic.com/",
  "license"      :  "LGPL-3",
  "description"  :  """
  Newlogic Location Module
  ========================

  - 
  
  """,
  "depends"      :  ['base','newlogic_main'],
  "data"         :  [
                  'security/ir.model.access.csv',
                  'views/registrants_view.xml',
                  'views/location.xml',
                    ],
  'assets'       :  {},
  "demo"         :  [],
  "images"       :  [],
  "application"  :  True,
  "installable"  :  True,
  "auto_install" :  False,
}
