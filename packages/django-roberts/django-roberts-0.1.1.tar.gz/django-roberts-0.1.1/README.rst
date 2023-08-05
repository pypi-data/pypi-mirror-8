django-roberts
==============

A simple Django app to serve a robots.txt file.


Installation
------------

Use your favorite Python installer to install it from PyPI::

    pip install django-roberts

Or get the source from the application site::

    hg clone https://bitbucket.org/mhurt/django-roberts
    
The :code:`robots` package, included in the distribution, should be placed on the :code:`PYTHONPATH`.


Configuration
-------------

1. Include the package's url patterns in your root :code:`urls.py`::

    url(r'', include('robots.urls')),

2. Add :code:`robots` to your :code:`INSTALLED_APPS` setting.

3. If your run Django's development server you should now be able to see the example robots.txt file at:

    http://127.0.0.1:8000/robots.txt


If you don't wish to use the supplied templates you can simply:

1. Remove :code:`robots` from your :code:`INSTALLED_APPS` setting;
2. Create your own template using the default location :code:`robots/robots.txt`


Extras
------

For convenience the package defines the usable combinations of robots directives which can be used in your views and templates.

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