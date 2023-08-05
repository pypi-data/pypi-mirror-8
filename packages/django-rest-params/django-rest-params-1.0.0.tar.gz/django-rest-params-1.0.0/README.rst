Django REST Params
==================

Function decorator to specify and validate parameters for API calls.
Invalid params will automatically return a useful error message;
validated params are passed to the wrapped function as kwargs.

A Few Examples
--------------------

Specify the types of parameters, and check that they are within acceptable ranges:

.. code:: python

   from django_rest_params.decorators import params
   
   @api_view(['GET'])
   @params(latitude=float, latitude__gte=-90.0, latitude__lte=90.0,
           longitude=float, longitude__gte=-180.0, longitude__lte=180.0)
   def get_something(request, latitude, longitude):
       # If latitude/longitude are missing or out of range, user will get an error message.
       # If we get here, we know they're valid
       pass

Create optional params with default values. Django REST Params supports POST params as well:

.. code:: python

   @api_view(['POST'])
   @params(offset=int, offset__default=0)
   def paged_api_call(request, offset):
       # if offset isn't specified, default value is used
       pass
       
Django REST Params works with ViewSets as well as request functions.

.. code:: python

   class ShirtsViewSet(viewsets.GenericViewSet):
   
       @params(colors=('red','blue','green','yellow'), colors__many=True, 
               colors__optional=True, colors__name='color_filter')
       def get_shirts(self, request, colors):
           # Handle API calls like these:
           # /shirts?color_filter=red          __name lets you use a function param name different from the API param name
           # /shirts?color_filter=yellow,blue  __many lets you pass multiple values
           # /shirts                           __optional will set colors to None if it isn't specified
           # /shirts?color_filter=black        ERROR! This will return an error stating black is invalid, and listing the valid options
           pass

Options
=======

TYPE
----
Specify the type of a param:

.. code:: python

   latitude=float

valid options are:
  - int
  - float
  - bool
  - str/unicode
  - tuple/list/set/frozenset (which will be treated as a list of valid options)
  - a django Model subclass (in which case the param will be treated as a PK to that Model)
  
GT/LT/GTE/LTE
-------------
Automatically check that a param falls within a certain range. Valid for float, int, or Model PK, which all do numerical comparisons.

.. code:: python

   latitude__gte=-90.0
   latitude__lte=90.0
  
LENGTH__LT/GT/LTE/GTE/EQ
------------------------
Only valid for str params. Check the length of the str

.. code:: python

  description__length__lt=256
  country_code__length__eq=2
  
OPTIONAL
--------

.. code:: python

   latitude__optional=True # same as latitude__default=None
   
Default is False; if set to True, this param will be checked for validity (it will still return a 400 if it doesn't pass gte checks, for example),
but will be passed to the wrapped function as None if it wasn't specified.

DEFAULT
-------

.. code:: python

   sort_by=('publisher_guides_count', 'most_recent')
   sort_by__default='publisher_guides_count'
   
Implies that this param is optional.
Specify a default value for this param if it isn't specified.
 
NAME
----
By default, we'll look for a param with the same name as the kwargs, e.g.

.. code:: python

   user_id=User # look for user_id param, create a User object and pass to wrapped fn as user_id
   
But sometimes it makes more sense to call such a param 'user', so you can do:

.. code:: python

   user=User, user__name='user_id' # look for user_id, assign to user
  
MANY
----

.. code:: python

   users=int # param 'users=1' is ok, 'users=1,2' is not
   users__many=True # param 'users=1,2' will return tuple of (1, 2), 'users=1' will return (1)
   
Allow User to (optionally) specify params as CSV (GET) or Array (JSON POST)
If many==True, the params will be returned as a tuple regardless of whether or not there was only one param

DEFERRED
--------
.. code:: python

   user__deferred=True

By default, Django REST Params will retrieve an object like this:

.. code:: python

   User.objects.only('id').get(id=user_id) # all fields except for 'id' are deferred

Usually, this is preferrable, since we usually don't need to fetch the entire object from the DB, and it is significantly faster than doing so.
By setting __deferred to False, Django REST Params will change the object retrieval call to this:

.. code:: python

    User.objects.get(id=user_id)  # All fields are fetched

FIELD
-----

.. code:: python

   category = Category # by default, do Category.get(id=category)
   category__field='name' # instead, do Category.get(name=category)
   
Applies to Django models only. By default, we treat the param as an ID; instead, you can treat it as something else, e.g. 'name'

METHOD
------
Valid methods for passing this param. Default is 'POST' for POST/PUT requests and GET for all others

.. code:: python

  user__method='GET' # GET only
  user__method=('GET', 'POST') # allow either source
  
  
Tests
=====
  
Run the (fairly extensive) unit tests:
  
.. code:: bash
  
   python -m tests.tests
   
Mock classes are used to simulate Django models / managers / Django REST Framework requests, so these tests don't actually need to run inside a Django app.
