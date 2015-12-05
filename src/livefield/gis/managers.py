from django.db import models
from .querysets import LiveGeoQuerySet


class LiveGeoManagerBase(models.Manager):
    # To also use this manager for FK lookups, see
    # https://docs.djangoproject.com/en/1.6/topics/db/managers/#manager-types.

    def __init__(self, include_soft_deleted=False, *args, **kwargs):
        self.include_soft_deleted = include_soft_deleted
        super(LiveGeoManagerBase, self).__init__(*args, **kwargs)  # pylint: disable=super-on-old-class

    def get_queryset(self):
        qs = super(LiveGeoManagerBase, self).get_queryset()  # pylint: disable=super-on-old-class
        if not self.include_soft_deleted:
            return qs.live()
        return qs


LiveGeoManager = LiveGeoManagerBase.from_queryset(LiveGeoQuerySet)
