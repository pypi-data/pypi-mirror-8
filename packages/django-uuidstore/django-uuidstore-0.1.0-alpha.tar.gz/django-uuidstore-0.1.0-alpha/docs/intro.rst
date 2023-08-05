.. _intro:


Getting Started
===============


Registering your model
----------------------

Somewhere at the end of your models.py add the following:

::

    # models.py
    from django.db import models


    class MyModel(models.Model):
        title = models.Charfield(max_length=60)


    import uuidstore
    uuidstore.register(MyModel)


With the code above ``MyModel`` is registered with uuidstore. When you save an
instance of your model for the first time, and new ObjectUUID will be created
containing a UUID and a generic-relation to your model instance.

Let's see how that works by running ``python manage.py shell``:

::

    >>> from myapp.models import MyModel
    >>> from uuidstore.models import ObjectUUID
    >>>
    >>> # Create an instance of your model
    >>> instance = MyModel.objects.create(title='Foo')
    >>>
    >>> # Retrieve the related ObjectUUID
    >>> stored = ObjectUUID.objects.get_for_instance(instance)
    >>> stored.uuid
    UUID('2f8c1da9030e45f1a58a52f988d0370c')

In this case we can see that the ObjectUUID has been created. The UUID itself
is only accessible by explicitly querying ObjectUUID. For most uses you'll
probably want the UUID accessible via the model instance itself. The following
examples show how this is achieved.


Monkey patching
---------------

This example shows how to both register your model *and* have the UUID
accessible as an attribute of your model.

::

    # models.py
    from django.db import models


    class MyModel(models.Model):
        title = models.Charfield(max_length=60)

    import uuidstore
    uuidstore.register(MyModel, uuid_descriptor='uuid')

The only thing we've changed with this code is to add a keyword argument
``uuid_descriptor`` to the registration call. This works as the previous
example, but this time the next instantiation of a MyModel object will look up
its UUID and attach it as a property of MyModel with the name you supplied.

Let's see how that works by running ``python manage.py shell``:

::

    import uuidstore
    uuidstore.register(MyModel, uuid_descriptor='uuid')

    >>> from myapp.models import MyModel
    >>> from uuidstore.models import ObjectUUID
    >>>
    >>> # Create an instance of your model
    >>> instance = MyModel.objects.create(title='Bar')
    >>>
    >>> # Retrieve the related ObjectUUID
    >>> stored = ObjectUUID.objects.get_for_instance(instance)
    >>> stored.uuid
    UUID('dbf1ee099cbf481b8fd431ecad0985be')
    >>>
    >>> # Unlike the first example, the UUID is now attached to your instance:
    >>> instance.uuid
    UUID('dbf1ee099cbf481b8fd431ecad0985be')

This works well for cases where you are unable to modify the base model itself,
but it's not very efficient as we're invoking a ContentType lookup for each
instance.


Denormalisation
---------------

Here we'll cut out some of the inefficiency of monkey patching by denormalising
the UUID to a CharField.

::

    # models.py
    from django.db import models


    class MyModel(models.Model):
        title = models.Charfield(max_length=60)
        uuid = models.CharField(max_length=36, blank=True, editable=False)


    import uuidstore
    uuidstore.register(MyModel, uuid_descriptor='uuid')



Let's see how that works by running ``python manage.py shell``:

::

    import uuidstore
    uuidstore.register(MyModel, uuid_descriptor='uuid')

    >>> from myapp.models import MyModel
    >>> from uuidstore.models import ObjectUUID
    >>>
    >>> # Create an instance of your model
    >>> instance = MyModel.objects.create(title='Fizz')
    >>>
    >>> # Retrieve the related ObjectUUID
    >>> stored = ObjectUUID.objects.get_for_instance(instance)
    >>> stored.uuid
    UUID('c2dd74463da242d9bc5d7a57f3dfc6dc')
    >>>
    >>> # Unlike the first example, the UUID is now attached to your instance:
    >>> instance.uuid
    u'c2dd74463da242d9bc5d7a57f3dfc6dc'


.. note::

   Unlike the other examples here, the denormalised UUID is, understandably,
   stored as a string.  It's quick and flexible but if you want a UUID object
   you'll need to convert it yourself, or revert to querying ObjectUUID
   directly.




Denormalisation to a UUID field
-------------------------------

::

    # models.py
    from django.db import models
    from uuidstore.fields import UUIDField


    class MyModel(models.Model):
        title = models.Charfield(max_length=60)
        uuid = UUIDField(auto=False, blank=True, null=True, unique=True)


    import uuidstore
    uuidstore.register(MyModel, uuid_descriptor='uuid')


In this case we've replaced the CharField from the previous example with
``uuidstore.fields.UUIDField``.  This is simply a convenience, and simply
references ``django_uuid_pk.fields.UUIDField``.

Let's see how that works by running ``python manage.py shell``:

::

    import uuidstore
    uuidstore.register(MyModel, uuid_descriptor='uuid')

    >>> from myapp.models import MyModel
    >>> from uuidstore.models import ObjectUUID
    >>>
    >>> # Create an instance of your model
    >>> instance = MyModel.objects.create(title='Buzz')
    >>>
    >>> # Retrieve the related ObjectUUID
    >>> stored = ObjectUUID.objects.get_for_instance(instance)
    >>> stored.uuid
    UUID('33057f5367064c92ae8d9f2c0dbe496c')
    >>>
    >>> # Unlike the first example, the UUID is now attached to your instance:
    >>> instance.uuid
    UUID('33057f5367064c92ae8d9f2c0dbe496c')


.. tip::

   You don't need to use the provided UUIDField. You can use your own, provided
   that uuidstore can set its value after it has been saved.
