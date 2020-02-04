.. _api_reference:

===============
 API Reference
===============

This section covers interfaces of Delair.ai Python SDK.

Main interface
==============

Entry point
-----------

Delair-Stack Python SDK has a unique entry point: The class
``DelairStackSDK``.

.. autoclass:: delairstack.sdk.DelairStackSDK
   :members: __init__

Configuration
-------------

.. autoclass:: delairstack.core.config.Config
   :members: __init__

.. autoclass:: delairstack.core.config.ConnectionConfig
   :members: __init__

Resources management
--------------------

.. autoclass:: delairstack.core.resources.resources_manager_base.ResourcesManagerBase
   :members:

.. autoclass:: delairstack.core.resources.resource.Resource
   :members: __init__

Errors
------

.. automodule:: delairstack.core.errors
   :members:

Annotations
===========

.. autoclass:: delairstack.apis.client.annotations.annotationsimpl.AnnotationsImpl
   :members:

Comments
========

.. autoclass:: delairstack.apis.client.comments.commentsimpl.CommentsImpl
   :members:

Datasets
========

.. autoclass:: delairstack.apis.client.datamngt.datasetsimpl.DatasetsImpl
   :members:

Missions
========

.. autoclass:: delairstack.apis.client.projectmngt.missionsimpl.MissionsImpl
   :members:

Mission resource
----------------

.. autoclass:: delairstack.core.resources.projectmngt.missions.Mission
   :members: __init__

Flight resource
----------------

.. autoclass:: delairstack.core.resources.projectmngt.flights.Flight
   :members: __init__

Projects
========
.. autoclass:: delairstack.apis.client.projectmngt.projectsimpl.ProjectsImpl
   :members:

Project resource
----------------

.. autoclass:: delairstack.core.resources.projectmngt.projects.Project
   :members: __init__

Tags
====

.. autoclass:: delairstack.apis.client.tags.tagsimpl.TagsImpl
   :members:
