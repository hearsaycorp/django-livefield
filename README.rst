================
django-livefield
================

.. image:: https://travis-ci.org/hearsaycorp/django-livefield.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/hearsaycorp/django-livefield

.. image:: https://pypip.in/v/django-livefield/badge.png
    :alt: Latest PyPI Version
    :target: https://pypi.python.org/pypi/django-livefield/

=====
About
=====
A Django field that enables convenient soft-deletion.

=============
Example Usage
=============
.. code:: python

    >>> from django.db import models
    >>> from django_livefield import LiveField, LiveManager
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
    >>> john = Person.objects.create(name='John Cleese')
    >>> doppelganger = Person(name='John')
    >>> doppelganger.save()  # Raises an IntegrityError
    >>> john.delete()
    >>> doppelganger.save()  # Succeeds!
