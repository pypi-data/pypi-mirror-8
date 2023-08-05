django-roberts
==============

A simple Django app to serve a robots.txt file.


Requirements
------------

Django 1.2 or greater, Python 2.7 or greater.


Installation
------------

Use your favorite Python installer to install it from PyPI::

    pip install django-roberts

Or get the source from the application site::

    hg clone https://bitbucket.org/mhurt/django-roberts
    
The :code:`robots` package, included in the distribution, should be placed on the :code:`PYTHONPATH`.



Configuration
-------------

1. Add :code:`robots` to your :code:`INSTALLED_APPS` setting.

2. Include the package's url patterns in your root :code:`urls.py`::

    url(r'', include('robots.urls')),

If your run Django's development server you should now be able to see the example robots.txt file at http://127.0.0.1:8000/robots.txt



Extras
------

For convenience the package defines the usable combinations of robots directives which can be used in your views and templates.

The following constants are defined:

* NOINDEX_FOLLOW
* INDEX_NOFOLLOW
* NOINDEX_NOFOLLOW

Here's a simple example of using these constants in practice...

In your view::

    # views.py
    import robots
    
    class MyView(ListView):
        meta_robots = robots.NOINDEX_FOLLOW
        ...
        ...

In your base template::

    # base.html
    <html>
      <head>
      ...
      {% include 'robots/meta_robots.html' %}
      
      <!-- OR -->
      
      {% if view.meta_robots %}
        <meta name="robots" content="{{ view.meta_robots }}">
      {% endif %}
      ...
      ...

Python package
--------------
The Python package is available from PyPI_ 


Get the source code
-------------------
From our `BitBucket repository`_.


Report a bug
------------
Please report any bugs through our `Issue Tracker`_.

.. _PyPI: https://pypi.python.org/pypi/django-roberts
.. _BitBucket repository: https://bitbucket.org/mhurt/django-roberts
.. _Issue Tracker: https://bitbucket.org/mhurt/django-roberts/issues
