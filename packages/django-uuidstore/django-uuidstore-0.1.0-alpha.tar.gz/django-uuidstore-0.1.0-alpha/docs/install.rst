.. _install:


Installation
============

Use your favorite Python installer to install it from PyPI::

    $ pip install django-uuidstore

If you are using ``pip`` version 1.4 or later you'll need to explicitly allow
pre-release installation::

    $ pip install --pre django-uuidstore

Or get the source from the application site::

    $ hg clone https://bitbucket.org/mhurt/django-uuidstore
    $ cd django-uuidstore
    $ python setup.py install

Configuration
-------------

Add ``"uuidstore"`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = {
      ...
      'uuidstore'
    }

For Django 1.7 users, run ``python manage.py migrate`` to create the
models. Otherwise simply run ``python manage.py syncdb``.


