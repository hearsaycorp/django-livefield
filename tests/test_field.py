from django.db import IntegrityError
from django.db import transaction
from django.test import TestCase

from .models import Person, Person2


class LiveFieldTests(TestCase):

    model = Person

    def test_inits_alive(self):
        o = self.model(name='test')
        self.assertTrue(o.live)

    def test_saving_retains_alive(self):
        o = self.model(name='test')
        o.save()
        o2 = self.model.all_objects.get(id=o.id)
        self.assertTrue(o2.live)

    def test_saving_retains_dead(self):
        o = self.model(name='test')
        o.live = False
        o.save()
        o2 = self.model.all_objects.get(id=o.id)
        self.assertFalse(o2.live)

    def test_truthy_values_dont_delete(self):
        for name, val in enumerate(['truthy', 11, 6L, True, (1, 3)]):
            obj = self.model(name=name)
            obj.live = val
            # Use 'is' to make sure that we're returning bools.
            self.assertTrue(obj.live is True)

    def test_falsy_values_delete(self):
        for name, val in enumerate(['', 0, False, {}, None]):
            obj = self.model(name=name)
            obj.live = val
            # Again, use 'is' to make sure that we're returning bools.
            self.assertTrue(obj.live is False)

    def test_allows_uniqueness_with_many_dead(self):
        first = self.model(name='collision')
        first.save()
        second = self.model(name='collision')
        # Uniqueness constraint should prevent a second live object with the
        # same name.
        with transaction.atomic():
            self.assertRaises(IntegrityError, second.save)

        # Should be able to have several dead objects with same name
        first.live = False
        first.save()
        # Now we can save and delete second
        second.save()
        second.live = False
        second.save()

        third = self.model(name='collision')
        third.save()
        self.assertEqual(self.model.all_objects.count(), 3)

        # Resurrecting one of the dead dupes should violate uniqueness
        first.live = True
        with transaction.atomic():
            self.assertRaises(IntegrityError, first.save)


class LiveFieldTests2(LiveFieldTests):
    model = Person2
