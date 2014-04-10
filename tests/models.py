from django.db import models

from django_livefield import LiveField, LiveManager, LiveModel


class Person(models.Model):
    name = models.CharField(max_length=20)
    live = LiveField()

    class Meta:
        unique_together = ('name', 'live')

    objects = LiveManager()
    all_objects = LiveManager(include_soft_deleted=True)



class Person2(LiveModel):
    name = models.CharField(max_length=20)

    class Meta:
        unique_together = ('name', 'live')
