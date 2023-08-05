# Django-roberts

A simple Django app to serve a robots.txt file.


## Installation

Use your favorite Python installer to install it from PyPI:

    pip install django-roberts

Or get the source from the application site:

    hg clone https://bitbucket.org/mhurt/django-roberts
    
The `robots` package, included in the distribution, should be placed on the `PYTHONPATH`.


## Configuration

Add `robots` to your `INSTALLED_APPS` setting.

Include the package's url patterns in your root urlconf:

    url(r'', include('robots.urls')),
    
If your run Django's development server you should now be able to see the example robots.txt file at

    http://127.0.0.1:8000/robots.txt
    
