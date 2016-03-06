from django.test import TestCase

from .models import Person


class LiveManagerTests(TestCase):

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

    def test_defaults_to_live_only(self):
        self.assertEqual(Person.objects.all().count(), 3)

    def test_alternate_manager_includes_soft_deleted(self):
        self.assertEqual(Person.all_objects.all().count(), 5)

    # Verify that our convenience functions are working as expected.

    def test_live_proxies_to_queryset(self):
        self.assertEqual(Person.all_objects.live().count(), 3)

    def test_non_dead_proxies_to_queryset(self):
        self.assertEqual(Person.all_objects.non_dead().count(), 3)

    def test_dead_proxies_to_queryset(self):
        self.assertEqual(Person.all_objects.dead().count(), 2)

    def test_soft_delete_proxies_to_queryset(self):
        Person.all_objects.soft_delete()
        self.assertEqual(Person.all_objects.dead().count(), 5)

    def test_hard_delete_proxies_to_queryset(self):
        Person.all_objects.hard_delete()
        self.assertEqual(Person.all_objects.count(), 0)

    def test_default_delete_proxies_to_queryset(self):
        Person.all_objects.delete()
        self.assertEqual(Person.all_objects.dead().count(), 5)
