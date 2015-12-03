from django.db import models

from .querysets import LiveGeoQuerySet


LiveGeoManagerBase = models.Manager.from_queryset(LiveGeoQuerySet)


class LiveGeoManager(LiveGeoManagerBase):
    # To also use this manager for FK lookups, see
    # https://docs.djangoproject.com/en/1.6/topics/db/managers/#manager-types.

    def __init__(self, include_soft_deleted=False, *args, **kwargs):
        self.include_soft_deleted = include_soft_deleted
        super(LiveGeoManager, self).__init__(*args, **kwargs)  # pylint: disable=super-on-old-class

    def get_queryset(self):
        qs = super(LiveGeoManager, self).get_queryset()  # pylint: disable=super-on-old-class
        if not self.include_soft_deleted:
            return qs.live()
        return qs
