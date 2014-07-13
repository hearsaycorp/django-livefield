from model_utils.managers import PassThroughManager

from .querysets import LiveGeoQuerySet


class LiveGeoManager(PassThroughManager):
    # To also use this manager for FK lookups, see
    # https://docs.djangoproject.com/en/1.6/topics/db/managers/#manager-types.

    def __init__(self, queryset_cls=LiveGeoQuerySet, include_soft_deleted=False, *args, **kwargs):
        self.include_soft_deleted = include_soft_deleted
        super(LiveGeoManager, self).__init__(queryset_cls=queryset_cls, *args, **kwargs)

    def get_queryset(self):
        qs = super(LiveGeoManager, self).get_queryset()
        if not self.include_soft_deleted:
            return qs.live()
        return qs
