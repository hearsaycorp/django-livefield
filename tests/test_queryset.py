import django
from django.test import TestCase

from .models import Person


class LiveQuerySetTests(TestCase):

    names = (
        'Graham Chapman',
        'John Cleese',
        'Terry Gilliam',
    )

    def setUp(self):
        # Create some soft-deleted records.
        for name in self.names[:2]:
            p = Person(name=name)
            p.live = False
            p.save()

        # And then create live records with the same names.
        for name in self.names:
            Person.objects.create(name=name)

    def test_live_filter(self):
        self.assertEqual(Person.all_objects.all().live().count(), 3)

    def test_non_dead_filter(self):
        self.assertEqual(Person.all_objects.all().non_dead().count(), 3)

    def test_dead_filter(self):
        self.assertEqual(Person.all_objects.all().dead().count(), 2)

    def test_soft_delete(self):
        deleted = Person.all_objects.all().soft_delete()
        self.assertEqual(deleted, 5)
        self.assertEqual(Person.all_objects.all().dead().count(), 5)

    def test_hard_delete(self):
        deleted = Person.all_objects.all().hard_delete()
        # Django 1.9+ returns number of deleted rows
        if django.VERSION >= (1, 9, 0):
            self.assertEqual(deleted, 5)
        else:
            # Older versions do not
            self.assertIsNone(deleted)
        self.assertEqual(Person.all_objects.all().count(), 0)

    def test_default_delete_is_soft(self):
        deleted = Person.all_objects.all().delete()
        self.assertEqual(deleted, 5)
        self.assertEqual(Person.all_objects.all().dead().count(), 5)
