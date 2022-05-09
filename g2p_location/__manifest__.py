# -*- coding: utf-8 -*-
#################################################################################
# Author      : Newlogic (<https://newlogic.com/>)
# Copyright(c): Newlogic
# All Rights Reserved.
#################################################################################
{
  "name"         :  "G2P Location Module",
  "category"     :  "G2P",
  "version"      :  "0.0.1",
  "sequence"     :  1,
  "author"       :  "Newlogic",
  "website"      :  "https://newlogic.com/",
  "license"      :  "Other OSI approved licence",
  "description"  :  """
  Newlogic Location Module
  ========================

  - 
  
  """,
  "depends"      :  ['base','g2p_registrant'],
  "data"         :  [
                  'security/ir.model.access.csv',
                  'views/individual_views.xml',
                  'views/group_views.xml',
                  'views/location.xml',
                  'views/location_import_views.xml',
                    ],
  'assets'       :  {},
  "demo"         :  [],
  "images"       :  [],
  "application"  :  True,
  "installable"  :  True,
  "auto_install" :  False,
}
