OpenG2P - Social Protection Solution
====================================

`OpenG2P` is an open-source project that aims to streamline the management of social protection programs.
It can be used on its own or in conjunction with other services.

.. image:: programs/images/openg2p_overview.png
  :alt: OpenG2P overview

`OpenG2P` is based on an open-source ERP called `Odoo 15.0 <https://odoo.com/documentation/15.0/>`_. It allows
the project to take advantage of a vast ecosystem of existing integrations and modules.

`OpenG2P` is currently in development, and everything is evolving rapidly as a result of our users' comments.
If you have any questions or needs, please do not hesitate to contact the team through Github discussion, Github
issues or through our `Website <https://newlogic.com/contact/>`_.


Getting started with OpenG2P
---------------------------------

:doc:`installing`
    How to install this project on your server.

:doc:`configuring`
    Project configuration and customization options.

Development
-----------

:doc:`contributing`
    How to contribute changes to the project.

:doc:`changelog`
    The project development changelog.

.. Hidden TOCs

.. toctree::
   :caption: Getting started
   :maxdepth: 2
   :hidden:

   installing
   architecture
   features
   contributing

.. toctree::
   :maxdepth: 1
   :hidden:

   changelog

.. toctree::
    :maxdepth: 2
    :caption: Registrants
    :hidden:

    registrants/concepts
    registrants/exporting
    registrants/importing
    registrants/api

.. toctree::
    :maxdepth: 2
    :caption: Programs
    :hidden:

    programs/concepts
    programs/dashboards
    programs/program_manager
    programs/cycle_manager
    programs/eligibility_manager
    programs/entitlement_manager
    programs/deduplication_manager
    programs/notification_manager


.. toctree::
    :maxdepth: 2
    :caption: Deduplication Service
    :hidden:

    deduplicator/index
    deduplicator/install
    deduplicator/gettingstarted

.. toctree::
    :maxdepth: 2
    :caption: Disbursement Service
    :hidden:

    disbursement/index

.. toctree::
    :maxdepth: 2
    :caption: Using
    :hidden:

    using/managing_users
    using/audit_logs
