django-selectable
===================

Tools and widgets for using/creating auto-complete selection widgets using Django and jQuery UI.

.. image:: https://travis-ci.org/mlavin/django-selectable.svg?branch=master
    :target: https://travis-ci.org/mlavin/django-selectable


Features
-----------------------------------

- Works with the latest jQuery UI Autocomplete library
- Auto-discovery/registration pattern for defining lookups


Installation Requirements
-----------------------------------

- Python 2.6-2.7, 3.2+
- `Django <http://www.djangoproject.com/>`_ >= 1.5
- `jQuery <http://jquery.com/>`_ >= 1.7
- `jQuery UI <http://jqueryui.com/>`_ >= 1.8

To install::

    pip install django-selectable

Next add `selectable` to your `INSTALLED_APPS` to include the related css/js::

    INSTALLED_APPS = (
        'contrib.staticfiles',
        # Other apps here
        'selectable',
    )

The jQuery and jQuery UI libraries are not included in the distribution but must be included
in your templates. See the example project for an example using these libraries from the
Google CDN.

Once installed you should add the urls to your root url patterns::

    urlpatterns = patterns('',
        # Other patterns go here
        (r'^selectable/', include('selectable.urls')),
    )


Documentation
-----------------------------------

Documentation for django-selectable is available on `Read The Docs <http://readthedocs.org/docs/django-selectable>`_.


Additional Help/Support
-----------------------------------

You can find additional help or support on the mailing list: http://groups.google.com/group/django-selectable


Contributing
--------------------------------------

If you think you've found a bug or are interested in contributing to this project
check out our `contributing guide <http://readthedocs.org/docs/django-selectable/en/latest/contribute.html>`_.

If you are interested in translating django-selectable into your native language
you can join the `Transifex project <https://www.transifex.com/projects/p/django-selectable/>`_.



