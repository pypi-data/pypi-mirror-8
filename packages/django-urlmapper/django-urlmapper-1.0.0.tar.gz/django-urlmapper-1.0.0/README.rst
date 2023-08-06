Django Urlmapper
================

Urlmapper is a library for Django to print out the registered urls for a
site in a readable format.

Basic Usage
-----------

.. code-block:: python

    from mysite.urls import urlpatterns
    from urlmapper.utils import get_urls

    urls = get_urls(urlpatterns)

    for entry in urls:
        print(entry["path"], entry["name"], entry["view"])


A urlpattern like:

.. code-block:: python

    extra = [
        url("^world/$", view),
    ]

    nested = [
        url(r"^(?P<slug>\w+)/", include([
            url(r"^$", view),
            url(r"^history/$", view),
            url(r"^edit/$", view),
        ])),
    ]

    urlpatterns = [
        url("^$", view),
        url("^product/(?P<slug>[^/]+)/$", view, name="product-detail"),
        url("^about/$", view, name="about"),
        url("^hello/", include(extra)),
        url("^page/", include(nested)),
    ]

Would output like:

::

    /
    /about/
    /hello/world/
    /page/<slug>/
    /page/<slug>/edit/
    /page/<slug>/history/
    /product/<slug>/


Installation
------------

Urlmapper can be installed from PyPI:

::
    
    pip install django-urlmapper


Credits
-------

This code was originally modified from the django-extensions library for
use in things other than Django management commands.
