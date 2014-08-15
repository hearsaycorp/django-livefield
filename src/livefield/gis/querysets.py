from django.contrib.gis.db.models.query import GeoQuerySet


class LiveGeoQuerySet(GeoQuerySet):

    def delete(self):
        # Override Django's built-in default.
        self.soft_delete()

    def soft_delete(self):
        self.update(live=False)

    def undelete(self):
        self.update(live=True)

    def hard_delete(self):
        # Default Django behavior.
        super(LiveGeoQuerySet, self).delete()

    def live(self):
        return self.filter(live=True)

    def non_dead(self):
        return self.live()

    def dead(self):
        return self.filter(live__isnull=True)
