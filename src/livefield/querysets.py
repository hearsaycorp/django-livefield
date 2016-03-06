from django.db import models


class LiveQuerySet(models.query.QuerySet):

    def delete(self):
        # Override Django's built-in default.
        return self.soft_delete()

    def soft_delete(self):
        return self.update(live=False)

    def hard_delete(self):
        # Default Django behavior.
        result = super(LiveQuerySet, self).delete()
        return result[0] if result else None

    def live(self):
        return self.filter(live=True)

    def non_dead(self):
        return self.live()

    def dead(self):
        return self.filter(live__isnull=True)
