vis package
===========

vis.admin module
----------------

.. automodule:: vis.admin
   :members:
   :undoc-members:
   :show-inheritance:

vis.models module
-----------------
The models.py module in a Django project is responsible for defining the database schema through Django's Object-Relational Mapping (ORM) system. It contains the model classes which represent the tables and their relationships in the database. Each model class corresponds to a database table, and the attributes of the class correspond to the table's columns.

.. autoclass:: vis.models.CustomUser
    :members: team, info

.. autoclass:: vis.models.Eval
   :members: System_id, Round, Query, Metric, Value, Team

* Meta class:
   * Enforces a unique constraint on System_id, Round, Query, and Metric.
   * Defines indexes on Round, Query, Metric, and System_id.

.. autoclass:: vis.models.Team
    :members: name, info

In summary : 

* Eval: Stores evaluation data, capturing various metrics and values associated with different systems, rounds, and queries. This model includes constraints to ensure unique combinations of certain fields and utilizes indexes to optimize query performance.
* Team: Stores information about different teams, which can be linked to evaluations through the Eval model.
* CustomUser: Extends the default user model to include additional fields like team and info, providing a way to store more user-related information.

vis.serializers module
----------------------
The serializers.py module in a Django project, particularly when using Django Rest Framework (DRF), is responsible for defining serializers. Serializers are used to convert complex data types, such as Django models, into native Python data types that can then be easily rendered into JSON, XML, or other content types. They also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.

.. automodule:: vis.serializers
   :members:
   :undoc-members:
   :show-inheritance:

vis.urls module
----------------------

The urls.py module in a Django project is responsible for mapping URLs to their corresponding views. It acts as a routing table that directs incoming HTTP requests to the appropriate view based on the URL pattern. This is crucial for defining the structure and navigation of a web application or API.

In the provided urls.py file, several routes are defined to handle different parts of the application:

1. Router Setup:

   * A DefaultRouter from Django Rest Framework is used to automatically generate URL patterns for viewsets.
   * Registers three viewsets with the router:
      * EvalViewSet for handling requests related to the Eval model.
      * TeamViewSet for handling requests related to the Team model.
      * CustomUserCreateView for handling requests related to the CustomUser model.

2. API Endpoints:

   * path('api/', include(router.urls)): Includes the automatically generated routes for the registered viewsets.
   * path('api/v1/', include('djoser.urls')): Includes Djoser's authentication-related URLs.
   * path('api/v1/', include('djoser.urls.authtoken')): Includes URLs for token-based authentication.

These routes allow the application to handle a variety of requests, both for the API and for the web front end, ensuring that each URL is correctly processed by the corresponding view function or class.

vis.views module
----------------
The views.py module in a Django project is responsible for handling the logic behind the application's web pages and API endpoints. It defines views, which are Python functions or classes that process HTTP requests, interact with models to retrieve or update data, and return HTTP responses.

In the provided views.py file, several classes and functions are defined to manage API calls and web page requests:

1. CustomUserCreateView: Manages API calls related to user creation, updating, and bulk deletion.
2. EvalViewSet: Handles API calls for the Eval model, including creating, deleting, and calculating average values.
3. TeamViewSet: Manages API calls for the Team model.

These views enable interaction with the backend database, allowing for CRUD (Create, Read, Update, Delete) operations on the Eval, Team, and User models. The module leverages Django Rest Framework to simplify the creation of RESTful APIs

.. automodule:: vis.views
   :members:
   :exclude-members: basename, description, detail, name, suffix, queryset
   :undoc-members:
   :show-inheritance:

