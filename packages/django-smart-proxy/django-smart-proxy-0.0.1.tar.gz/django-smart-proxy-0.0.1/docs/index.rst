Django Smart Proxy
=================

.. * `Bugs <https://github.com/celerityweb/django-smart-proxy/issues/>`_

.. contents::

.. toctree::
   :maxdepth: 1

   installation
   settings
   changes
   license

.. comment: split here

Overview and License
--------------------

Django Smart Proxy provides simple HTTP proxy functionality for the Django web
development framework.

It is based on Django HTTP Proxy, which was originally
written by Yuri van der Meer, inspired by `a blog post by Will Larson
<http://lethain.com/entry/2008/sep/30/suffer-less-by-using-django-dev-server-as-a-proxy/>`_.

It is licensed under an `MIT-style permissive license <license.html>`_ and
maintained on Github:

https://github.com/celerityweb/django-smart-proxy/


What It Does
------------

Django Smart Proxy allows you make requests to an external server by requesting
them from the main server running your Django application. In addition, it
allows you to record the responses to those requests and play them back at any
time.

One possible use for this application (actually, the reason it was developed)
is to allow for easy development of Ajax applications against a live server
environment:

* Avoid typical cross-domain issues while developing an Ajax application based
  on live data from another server.
* Record responses and play them back at a later time:
    * Use "live" data, even when you are developing offline
    * Speedy responses instead of having to wait for a remote server
* Manually edit record responses via the Django admin interface

Combined with the standard `Django development server <http://docs.djangoproject.com/en/dev/ref/django-admin/#runserver>`_,
you have a powerful (but easy to set up) toolbox for developing Ajax applications.

Contributing
------------

If you have any contributions, feel free to fork Django Smart Proxy on
Github

https://github.com/celerityweb/django-smart-proxy/
