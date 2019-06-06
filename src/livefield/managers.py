from django.db import models

from .querysets import LiveQuerySet


class LiveManagerBase(models.Manager):
    # To also use this manager for FK lookups, see
    # https://docs.djangoproject.com/en/1.6/topics/db/managers/#manager-types.

    def __init__(self, include_soft_deleted=False, *args, **kwargs):
        self.include_soft_deleted = include_soft_deleted
        super(LiveManagerBase, self).__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super(LiveManagerBase, self).get_queryset()
        if not self.include_soft_deleted:
            return qs.live()
        return qs


LiveManager = LiveManagerBase.from_queryset(LiveQuerySet)
