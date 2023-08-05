|Build Status|

MongoSQL
========

`SqlAlchemy <http://www.sqlalchemy.org/>`__ queries with MongoDB-style.

Extremely handy if you want to expose limited querying capabilities with
a JSON API while keeping it safe against SQL injections.

Tired of adding query parameters for pagination, filtering, sorting?
Here is the ultimate solution.

Table of Contents
=================

-  MongoSQL
-  Table of Contents
-  Querying

   -  Query Object Syntax
   -  Operations

      -  Projection Operation
      -  Sort Operation
      -  Group Operation
      -  Filter Operation
      -  Join Operation
      -  Aggregate Operation

   -  JSON Column Support

-  MongoQuery

   -  Starting Up
   -  Querying

-  CRUD Helpers

   -  CrudHelper
   -  StrictCrudHelper
   -  CrudViewMixin

Querying
========

MongoSQL follows `MongoDB query
operators <http://docs.mongodb.org/manual/reference/operator/query/>`__
syntax with custom additions.

Source for syntax handlers:
`mongosql/statements.py <mongosql/statements.py>`__

Query Object Syntax
-------------------

Querying is made with *Query Objects*: a dictionary which defines how to
perform a query.

-  ``project``: `Projection Operation <#projection-operation>`__
-  ``sort``: `Sort Operation <#sort-operation>`__
-  ``group``: `Group Operation <#group-operation>`__
-  ``filter``: `Filter Operation <#filter-operation>`__
-  ``join``: `Join Operation <#join-operation>`__
-  ``aggregate``: `Aggregate Operation <#aggregate-operation>`__
-  ``skip``, ``limit``: Rows slicing: skipping and limiting.
   ``skip=10, limit=100`` will result in
   ``SELECT .. LIMIT 100 OFFSET 10``.
-  ``count``: Instead of producing results, just count the number of
   rows. Specify ``1`` to enable counting, ``0`` to disable (the
   default).

An example Query Object is:

.. code:: python

    {
      'project': ['id', 'name'],  # Only fetch these columns
      'sort': ['age+'],  # Sort by age, ascending
      'filter': {
        # Filter condition
        'sex': 'female',  # Girls
        'age': { '$gte': 18 },  # Age >= 18
      },
      'join': ['articles'],  # Load 'articles' relationship
      'limit': 100,  # Display 100 per page
      'skip': 10,  # Skip first 10
    }

Detailed syntax for every operation is given below.

Operations
----------

Projection Operation
~~~~~~~~~~~~~~~~~~~~

Projection operation allows to specify which columns to include/exclude
in the result set.

Produces the following queries through SqlAlchemy:

::

    SELECT a, b           FROM ...;
    SELECT      c, d, ... FROM ...;

-  Dictionary syntax.

Specify field names mapped to boolean values: ``1`` for inclusion, ``0``
for exclusion.

::

    ```python
    { 'a': 1, 'b': 1 }  # Include specific fields. All other fields are excluded
    { 'a': 0, 'b': 0 }  # Exclude specific fields. All other fields are included
    ```

-  List syntax.

   List field names to include.

   .. code:: python

       [ 'a', 'b' ]  # Include these fields only

Sort Operation
~~~~~~~~~~~~~~

Sort rows.

Produces the following queries through SqlAlchemy:

::

    SELECT ... FROM ... ORDER BY a ASC, b DESC, ...;

-  Dictionary syntax.

   Map column names to sort direction: ``-1`` for ``DESC``, ``+1`` for
   ``ASC``:

   .. code:: python

       from collections import OrderedDict
       OrderedDict({ 'a': +1, 'b': -1 })

-  List syntax.

   List column names, optionally suffixed by the sort direction: ``-``
   for ``DESC``, ``+`` for ``ASC``:

   .. code:: python

       [ 'a+', 'b-', 'c' ]  # = { 'a': +1, 'b': -1, 'c': +1 }

Group Operation
~~~~~~~~~~~~~~~

Group rows.

Produces the following queries through SqlAlchemy:

::

    SELECT ... FROM ... GROUP BY a, b DESC, ...;

Syntax: same as for `Sort Operation <#sort-operation>`__.

Filter Operation
~~~~~~~~~~~~~~~~

Supports most of `MongoDB query
operators <http://docs.mongodb.org/manual/reference/operator/query/>`__,
including array behavior (for PostgreSQL).

Produces the following queries through SqlAlchemy:

::

    SELECT ... FROM ... WHERE ...<filtering-conditions>...;

Supports the following MongoDB operators:

-  ``{ a: 1 }`` - equality check. For array: containment check.

   For scalar column: ``col = value``.

   For array column: contains value: ``ANY(array_col) = value``.

   For array column and array value: array equality check:
   ``array_col = value``.

-  ``{ a: { $lt: 1 } }`` - <
-  ``{ a: { $lte: 1 } }`` - <=
-  ``{ a: { $ne: 1 } }`` - inequality check. For array: not-containment
   check.

   For scalar column: ``col != value``.

   For array column: does not contain value:
   ``ALL(array_col) != value``.

   For array column and array value: array inequality check:
   ``array_col != value``.

-  ``{ a: { $gte: 1 } }`` - >=
-  ``{ a: { $gt: 1 } }`` - >
-  ``{ a: { $in: [...] } }`` - any of. For arrays: intersection check.

   For scalar column: ``col IN(values)``

   For array column: ``col && ARRAY[values]``

-  ``{ a: { $nin: [...] } }`` - none of. For arrays: empty intersection
   check.

   For scalar column: ``col NOT IN(values)``

   For array column: ``NOT( col && ARRAY[values] )``

-  ``{ a: { $exists: true } }`` - ``IS [NOT] NULL`` check

-  ``{ arr: { $all: [...] } }`` - For array columns: contains all values
-  ``{ arr: { $size: 0 } }`` - For array columns: has a length of N

Supports the following boolean operators:

-  ``{ $or: [ {..criteria..}, .. ] }`` - any is true
-  ``{ $and: [ {..criteria..}, .. ] }`` - all are true
-  ``{ $nor: [ {..criteria..}, .. ] }`` - none is true
-  ``{ $not: { ..criteria.. } }`` - negation

Join Operation
~~~~~~~~~~~~~~

Allows to eagerly load specific relations by name.

-  List syntax.

   Relation names list.

   .. code:: python

       [ 'posts', 'comments' ]

-  Dict syntax, query on relations.

   Further, you can apply operations to relations using `Query Object
   Syntax <#query-object-syntax>`__!

   Map relation name to a Query Object, and the specified operations
   will be applied to related entities:

   .. code:: python

       {
         'posts': {  # Load relation 'posts'
           'filter': { 'id': { '$gt': 100 } },  # Only load posts with id > 100
           'sort': ['id-'],
           'skip': 0,
           'limit': 100,
           # ... see Query Object Syntax
         },
         'comments': None,  # No specific options, just load
       }

   Note that no relations are loaded implicitly: you need to specify
   them in a ``'join'``.

Aggregate Operation
~~~~~~~~~~~~~~~~~~~

Allows to fetch aggregated values with the help of aggregation
functions.

Dict syntax: custom name of the computed field mapped to an expression:

::

    { computed-field-name: expression }

The ** can be:

-  Column name
-  Aggregation operator:

   -  ``{ $min: operand }`` -- smallest value
   -  ``{ $max: operand }`` -- largest value
   -  ``{ $avg: operand }`` -- average value
   -  ``{ $sum: operand }`` -- sum of values

   The ** can be:

   -  Column name
   -  Boolean expression: see `Filter Operation <#filter-operation>`__
   -  Integer value (only supported by ``$sum`` operator)

Examples:

.. code:: python

    # Count people by age
    # NOTE: should be used together with grouping by 'age'
    {
      'age': 'age',  # Column value
      'n': { '$sum': 1 },  # Count
    }  # -> SELECT age, count(*) AS n ...

    # Average salary by profession
    # NOTE: should be used together with grouping by 'profession'
    {
      'prof': 'profession',
      'salary': { '$avg': 'salary' }
    }  # -> SELECT profession AS prof, avg(salary) AS salary ...

    # Count people matching certain conditions
    {
      'adults':    { '$sum': { 'age': { '$gte': 18 } } },
      'expensive': { '$sum': { 'salary': { '$gt': 10000 } } }
    }  # -> SELECT SUM(age >= 18) AS adults, SUM(salary > 10000) AS expensive ...

JSON Column Support
-------------------

PostgreSQL 9.3 supports `JSON & JSONB column
types <http://www.postgresql.org/docs/9.3/static/functions-json.html>`__,
and so does MongoSQL! :)

To access sub-properties of a JSON field, use dot-notation.

Given a model field:

.. code:: python

    model.data = { 'rating': 5.5, 'list': [1,2,3], 'obj': {'a': 1} }

You can reference JSON field properties:

.. code:: python

    'data.rating'
    'data.list.0'
    'data.obj.a'
    'data.obj.z'  # gives NULL

Operations that support it:

-  `Sort <#sort-operation>`__ and `Group <#group-operation>`__
   operations:

   .. code:: python

       ['data.rating-']

-  `Filter <#filter-operation>`__ operation:

   .. code:: python

       { 'data.rating': { '$gte': 5.5 } }
       { 'data.rating': None }  # Test for missing property

-  `Aggregation <#aggregation>`__:

   .. code:: python

       { 'max_rating': { '$max': 'data.rating' } }

*NOTE*: PostgreSQL is a bit capricious about data types, so MongoSql
tries to guess it using the operand you provide. Hence, when filtering
with a property known to contain a ``float``-typed field, provide
``float`` values to it.

MongoQuery
==========

Source: `mongosql/query.py <mongosql/query.py>`__

Starting Up
-----------

``MongoQuery`` is the interface to be used for querying with safe JSON
objects. It relies on ``MongoModel``: a wrapper for SqlAlchemy models
that holds cached data and build pieces for the query.

To enable MongoQuery in your application, you have two options:

1. *(low-level)* Construct ``MongoQuery`` manually from your model:

   .. code:: python

       from mongosql import MongoQuery
       from .models import User  # Your model

       ssn = Session()

       mq = MongoQuery.get_for(
           User,  # Model
           ssn.query(User)  # Initial query to start with
       )

   This will create and cache ``MongoModel`` for you.

2. *(high-level)* Use convenience mixin for your Base:

   .. code:: python

       from sqlalchemy.ext.declarative import declarative_base
       from mongosql import MongoSqlBase

       Base = declarative_base(cls=(MongoSqlBase,))

       class User(Base):
           #...

   Using this Base, your models will have a shortcut method which
   returns ``MongoQuery``:

   ::

       User.mongoquery(session)
       User.mongoquery(query)

   With ``mongoquery()``, you can construct a query from a session:

   .. code:: python

       mq = User.mongoquery(session)

   .. or from an
   `sqlalchemy.orm.Query <http://docs.sqlalchemy.org/en/latest/orm/query.html>`__,
   which allows you to apply some initial filtering:

   .. code:: python

       mq = User.mongoquery(
           session.query(User).filter_by(active=True)  # Only query active users
       )

Querying
--------

Having a ``MongoQuery``, you need just two methods:

-  ``query(**query_object)``: Make queries with a `Query
   Object <#query-object-syntax>`__ provided as keyword arguments.
-  ``end()``: Get the resulting
   `Query <http://docs.sqlalchemy.org/en/latest/orm/query.html>`__,
   ready for execution

``AssertionError`` is raised for validation errors, e.g. an unknown
field is provided by the user. No SQL stuff is ever contained in this
error: it's safe to display it to the user.

Example:

.. code:: python

    # QueryObject
    query_object = {
      'filter': {
        'sex': 'f', 
        'age': { '$gte': 18, '$lte': 25 },  # 18..25 years
      },
      'order': ['weight+'],  #  slims first
      'limit': 50,  # just enough :)
    }

    # MongoQuery
    q = User.mongoquery(session) \
        .query(**query_object) \
        .end()

    # Execute the query
    girls = q.all()

In addition, ``MongoQuery`` has chainable methods for every Query Object
Operation:

.. code:: python

    q = User.mongoquery(session) \
        .filter({'sex': 'f', 'age': { '$gte': 18, '$lte': 25 }}) \
        .order(['weight+']) \
        .limit(50) \
        .end()
    girls = q.all()

CRUD Helpers
============

MongoSql is designed to help with data selection for the APIs, and these
usually offer CRUD operations.

To ease the pain of implementing CRUD for all of your models, MongoSQL
comes with a CRUD helper that exposes MongoSQL capabilities for
querying. Together with
`RestfulView <https://github.com/kolypto/py-flask-jsontools#restfulview>`__
from
`flask-jsontools <https://github.com/kolypto/py-flask-jsontools>`__,
CRUD controllers are extremely easy to build.

CrudHelper
----------

Source: `mongosql/crud.py <mongosql/crud.py>`__

``CrudHelper`` is a helper class that contains parts of CRUD logic that
can be used in CRUD views.

You just instantiate it over an SqlAlchemy model:

.. code:: python

    from .models import User
    from mongosql import CrudHelper

    user_crudhelper = CrudHelper(User)

and now the following methods are available:

-  ``mquery(query, query_obj=None)``: Construct
   ```MongoQuery`` <#mongoquery>`__ for the model, using ``query`` as
   the intial Query. ``query_obj`` is the optional `Query
   Object <#query-object-syntax>`__.
-  ``create_model(entity)``: Create an SqlAlchemy instance from
   ``entity`` dictionary.
-  ``update_model(entity, prev_instance)``: Update an existing
   SqlAlchemy instance with some fields from the provided ``entity``
   dictionary.

   With PostgreSQL JSON fields, it has an additional feature:
   dictionaries are shallowly merged together. This way,
   ``update_model()`` allows you to add certain fields without loading
   the entity.

``AssertionError`` is raised for validation errors, e.g. an unknown
field is provided by the user.

StrictCrudHelper
----------------

Source: `mongosql/crud.py <mongosql/crud.py>`__

Usually it's not safe to allow changing all fields, loading all
relations, listing thousands of entities, etc.

``StrictCrudHelper`` subclasses ```CrudHelper`` <#crudhelper>`__ and
adds strict limitations to the things the user can do with your models.

Its constructor accepts the following additional arguments:

-  ``ro_fields=()``: List of read-only fields or field names. The user
   is not allowed to change or define these.

   Alternatively, this can be a callable which returns the list of
   read-only fields at runtime (e.g. in case this depends on the current
   user permissions).

-  ``allow_relations=()``: List of relations of relation names the user
   is allowed to `join <#join-operation>`__.

   All `joins <#join-operation>`__ in `Query
   Objects <#query-object-syntax>`__ are then checked against the list,
   and the user can never request a relation that's not explicitly
   allowed with this list.

   It supports relations on the parent model, as well as relations on
   sub-models using the dot-notation syntax (see the example below).

-  ``query_defaults=None``: Provide default values for the `Query
   Object <#query-object-syntax>`__ in case certain fields are not
   provided by the user.

   A good idea is to specify the default sorting fields and direction.
   The user can override it with his custom `Query
   Objects <#query-object-syntax>`__.

-  ``maxitems=None``: Set a hard limit on the number of entities the
   user can load.

   This value cannot be overridden with a `Query
   Object <#query-object-syntax>`__: the user will never load more than
   ``maxitems`` entities with a single query.

``AssertionError`` is raised for validation errors when the user tries
to hit the limits.

Example:

.. code:: python

    from .models import User
    from mongosql import StrictCrudHelper

    user_crudhelper = StrictCrudHelper(User,
        # Don't allow to change the primary key, and some secured fields
        ro_fields=('id', 'is_admin'),
        # Only allow to load the specified relations
        # In addition, allow some sub-relations
        allow_relations=(
            'articles',
            'comments',
            'articles.comments',  # sub-relation 'comments' on articles
        ),
        # Query Object defaults
        query_defaults = {
            'sort': ['id-'],  # id DESC
        },
        # Max 100 entities with a list query
        maxitems=100
    )

Having the limits specified, just use ```CrudHelper`` <#crudhelper>`__
methods and enjoy security.

CrudViewMixin
-------------

Source: `mongosql/crud.py <mongosql/crud.py>`__

```CrudHelper`` <#crudhelper>`__ itself if not the end-product: you
still need a view to manage your models.

``CrudViewMixin`` is a mixin for class-based views that leverages
```CrudHelper`` <#crudhelper>`__ and ```MongoQuery`` <#mongoquery>`__ to
create a perfect, dynamic API endpoint.

Have a look at
`flask.ext.jsontools.RestfulView <https://github.com/kolypto/py-flask-jsontools#restfulview>`__:
they are designed to be a perfect couple, so our example will use both.

When subclassing ``CrudViewMixin``, you need to do the following:

1. Initialize the ``crudhelper`` attribute with a
   ```CrudHelper`` <#crudhelper>`__ or
   ```StrictCrudHelper`` <#strictcrudhelper>`__
2. Override the ``_query()`` method, so ``CrudViewMixin`` knows how to
   get the database session
3. Implement CRUD methods using
   ``_method_list|create|get|update|delete()`` helpers
4. If required, implement
   ``_save_hook(new_instance, prev_instance=None)`` to handle cases when
   an entity is going to be saved (created or updated)

A full-featured and tested example:
`tests/crud\_view.py <tests/crud_view.py>`__. It's still quite verbose,
so make sure you create another base view for your application :)

.. |Build Status| image:: https://api.travis-ci.org/kolypto/py-mongosql.png?branch=master
   :target: https://travis-ci.org/kolypto/py-mongosql


