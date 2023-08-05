|Travis Status|

|Coverage Status|

|Downloads|

|Version|

|Violations|

|Requirements Status|

Django Mptt Admin
=================

*Django-mptt-admin* provides a nice Django Admin interface for Mptt
models. The source is available on
https://github.com/leukeleu/django-mptt-admin. It uses the
`jqTree <http://mbraak.github.io/jqTree/>`__ library.

Requirements
------------

The package is tested with Django (1.4 - 1.7), and Mptt (0.6.0, 0.6.1). Also with Python 2.6, 2.7 and 3.3, 3.4.

-  This version is not compatible with Django 1.3. Please use
   django-mptt-admin 0.1.2 for Django 1.3 support.

Installation
------------

Install the package:

::

    $ pip install django_mptt_admin

Add **django\_mptt\_admin** to your installed apps in **settings.py**.

::

    INSTALLED_APPS = (
        ..
        'django_mptt_admin',
    )

Use the DjangoMpttAdmin class in admin.py:

::

    from django.contrib import admin
    from django_mptt_admin.admin import DjangoMpttAdmin
    from models import Country

    class CountryAdmin(DjangoMpttAdmin):
        pass

    admin.site.register(Country, CountryAdmin)

Changelog
---------

**0.1.9** (july 12 2014)

- Issue 25: update jqtree to 0.21.0
- Issue 28: fixing problems related to working with model's pk-field, named other than "id" (thanks to Igor Gai)
- Issue 29: fix path to spinner.gif (thanks to Igor Gai)

**0.1.8** (februari 2 2014)

-  Issue 17: handle error when moving node
-  Issue 18: do not use inline javascript
-  Issue 19: support Django 1.7 alpha

**0.1.7** (january 3 2014)

-  Issue 16: moving a node fails if the node id is a uuid

**0.1.6** (october 10 2013)

-  Issue 8: removing node from the tree causes the tree view to crash

**0.1.5** (august 27 2013)

-  Issue 6: save the tree state
-  Issue 7: do not handle the right mouse click

**0.1.4** (august 8 2013)

-  Issue 5: Support for uuid ids

**0.1.3** (may 2 2013)

*This version drops support for Django 1.3.7*

-  Issue 2: Posting a screenshot in the readme would be really useful
   (thanks to Andy Baker)
-  Issue 3: Use static templatetag for CDN-compatible file paths (thanks
   to Alex Holmes)
-  Added
   `Coveralls <https://coveralls.io/r/leukeleu/django-mptt-admin>`__
   support

**0.1.2** (march 12 2013)

-  Issue 1: Grid view doesn't link correctly to object change pages
   (thanks to Kris Fields)

**0.1.1** (februari 25 2013)

-  Added experimental Python 3 support

**0.1** (februari 7 2013)

-  Initial version

|Bitdeli Badge|

.. |Travis Status| image:: https://secure.travis-ci.org/leukeleu/django-mptt-admin.png
   :target: http://travis-ci.org/leukeleu/django-mptt-admin
.. |Coverage Status| image:: https://coveralls.io/repos/leukeleu/django-mptt-admin/badge.png?branch=master
   :target: https://coveralls.io/r/leukeleu/django-mptt-admin
.. |Downloads| image:: https://pypip.in/d/django-mptt-admin/badge.png
   :target: https://pypi.python.org/pypi/django-mptt-admin/
.. |Version| image:: https://pypip.in/v/django-mptt-admin/badge.png
   :target: https://pypi.python.org/pypi/django-mptt-admin/
.. |Violations| image:: https://coviolations.io/projects/leukeleu/django-mptt-admin/badge/?
   :target: http://coviolations.io/projects/leukeleu/django-mptt-admin/
.. |Requirements Status| image:: https://requires.io/github/leukeleu/django-mptt-admin/requirements.png?branch=master
   :target: https://requires.io/github/leukeleu/django-mptt-admin/requirements/?branch=master
.. |Bitdeli Badge| image:: https://d2weczhvl823v0.cloudfront.net/leukeleu/django-mptt-admin/trend.png
   :target: https://bitdeli.com/free
