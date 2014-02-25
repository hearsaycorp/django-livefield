from model_utils.managers import PassThroughManager

from .live_queryset import LiveQuerySet


class LiveManager(PassThroughManager):
    # To also use this manager for FK lookups, see
    # https://docs.djangoproject.com/en/1.6/topics/db/managers/#manager-types.

    def __init__(self, queryset_cls=LiveQuerySet, include_soft_deleted=False, *args, **kwargs):
        self.include_soft_deleted = include_soft_deleted
        super(LiveManager, self).__init__(queryset_cls=queryset_cls, *args, **kwargs)

    def get_queryset(self):
        qs = super(LiveManager, self).get_queryset()
        if not self.include_soft_deleted:
            return qs.live()
        return qs

    # For convenience, Django treats calls to Person.objects.filter(...) as
    # calls to Person.objects.all().filter(...) (likewise for exclude, values,
    # etc.). Implement the same convenience layer for the special queryset
    # methods we've added.

    def soft_delete(self, *args, **kwargs):
        return self.get_queryset().soft_delete(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        return self.get_queryset().hard_delete(*args, **kwargs)

    def live(self):
        return self.get_queryset().live()

    def non_dead(self):
        return self.get_queryset().non_dead()

    def dead(self):
        return self.get_queryset().dead()
