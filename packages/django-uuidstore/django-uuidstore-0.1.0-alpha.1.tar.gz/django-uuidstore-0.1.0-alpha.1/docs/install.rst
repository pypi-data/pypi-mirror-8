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

- For Django 1.7 users, run
  ``python manage.py migrate uuidstore``
  to create the models.

- If you're using South, please see :ref:`withsouth`.

- Otherwise simply run ``python manage.py syncdb``.


.. _withsouth:

South Migrations
----------------

If you're using Django 1.7 you won't need to use South as migrations are built in.

If you're using an earlier version of Django with South 1.0 the provided
south_migrations will be automatically detected.

For earlier versions of South you'll need to tell explicitly define which
migrations to use by adding to, or creating, the ``SOUTH_MIGRATION_MODULES`` in
your settings file::

    # settings.py
    ...
    SOUTH_MIGRATION_MODULES = {
        'uuidstore': 'uuidstore.south_migrations',
    }

Don't worry, though, as running running a ``migrate`` will complain loudly if
you've forgotten this step.
