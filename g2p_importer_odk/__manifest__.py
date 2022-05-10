# -*- coding: utf-8 -*-
#################################################################################
# Author      : Newlogic (<https://newlogic.com/>)
# Copyright(c): Newlogic
# All Rights Reserved.
#################################################################################
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
                    'data/import_backend.xml',
                    'data/import_type.xml',
                    'data/import_source.xml',
                    'data/import_recordset.xml',
  ],
  "application"  :  True,
  "installable"  :  True,
  "auto_install" :  False,
}