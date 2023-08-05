Django uuidstore
================

A small Django app providing project-wide issue and storage of UUIDs.

.. warning::

   This is an early alpha release, and not intended for production use.

   *Use at your own risk!*


Dependencies
------------

UID-Store currently depends on
`django-uuid-pk 0.2 <https://pypi.python.org/pypi/django-uuid-pk/0.2>`_ .



Installation
------------

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

Add ``'uuidstore'`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = {
      ...
      'uuidstore'
    }

For Django 1.7 users, run ``python manage.py migrate`` to create the
models. Otherwise simply run ``python manage.py syncdb``.


Getting Started
---------------

First you'll need to register your model with uuidstore: ::

    # models.py
    ...
    ...
    import uuidstore
    uuidstore.register(MyModel)

From this point onwards each time a MyModel instance is saved uuidstore will
detect it and, if create new ObjectUUID instance containing a UUID relating
your model instance.
