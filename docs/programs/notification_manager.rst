***************************************
Notification Manager
***************************************
.. currentmodule:: g2p_programs.models.managers.notification_manager

The notification managers allow notifying beneficiaries of some events hapening in the programs or cycles.

:mod:`g2p_programs.models.managers.notification_manager` provides the class  :class:`BaseNotificationManager` define
the interface for this manager. :class:`SMSNotificationManager` is the default implementation.

.. autoclass:: BaseNotificationManager
    :members:

.. autoclass:: SMSNotificationManager
    :members:
    :undoc-members:

.. autoclass:: SMSTemplate
    :members:
    :undoc-members:
