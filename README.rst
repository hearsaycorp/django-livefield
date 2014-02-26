================
django-livefield
================

.. image:: https://magnum.travis-ci.com/hearsaycorp/django-livefield.png?token=pLaFnRxzmb8LMHcdgP2V
    :alt: Build Status
    :target: https://travis-ci.org/hearsaycorp/django-livefield

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
    ...    def delete(self):
    ...        self.live = False
    ...        self.save()
    ...
    >>> john = Person.objects.create(name='John Cleese')
    >>> doppelganger = Person(name='John Cleese')
    >>> doppelganger.save()  # Raises an IntegrityError
    >>> john.delete()
    >>> doppelganger.save()  # Succeeds!
