from django.test import TestCase

from .models import Item


class LiveModelTests(TestCase):

    def test_delete(self):
        item = Item.objects.create()
        item.delete()
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(Item.all_objects.count(), 1)
        self.assertEqual(Item.objects.filter(live__isnull=False).count(), 0)

    def test_hard_delete(self):
        item = Item.objects.create()
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.all_objects.count(), 1)
        item.hard_delete()
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(Item.all_objects.count(), 0)
