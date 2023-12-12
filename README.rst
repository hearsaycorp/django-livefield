================
django-livefield
================

=====
About
=====
A Django field that enables convenient soft-deletion. For Python 2.7/3.3+ and Django 1.8+

============
Installation
============
Simple: ``pip install django-livefield``.

=============
Example Usage
=============
.. code:: python

    >>> from django.db import models
    >>> from livefield import LiveField, LiveManager
    >>>
    >>>
    >>> class Person(models.Model):
    ...    name = models.CharField()
    ...    live = LiveField()
    ...
    ...    objects = LiveManager()
    ...    all_objects = LiveManager(include_soft_deleted=True)
    ...
    ...    class Meta:
    ...        unique_together = ('name', 'live')
    ...
    ...    def delete(self, using=None):
    ...        self.live = False
    ...        self.save(using=using)
    ...
    >>> john = Person.objects.create(name='John Cleese')
    >>> doppelganger = Person(name='John Cleese')
    >>> doppelganger.save()  # Raises an IntegrityError
    >>> john.delete()
    >>> doppelganger.save()  # Succeeds!

=======
License
=======
MIT. See LICENSE.txt for details.

============
Contributing
============
Pull requests welcome! To save everyone some hassle, please open an
issue first so we can discuss your proposed change.

In your PR, be sure to add your name to AUTHORS.txt and include some
tests for your spiffy new functionality.  CI will green-light your
build once it passes the unit tests (``./setup.py test``) and our
linters (``./lint.sh``).
