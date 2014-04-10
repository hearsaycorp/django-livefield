from django.db.models import Model
from django.contrib.gis.db.models import Model as GeoModel

from .fields import LiveField
from .managers import LiveManager, LiveGeoManager


class LiveModel(Model):
    live = LiveField()

    objects = LiveManager()
    all_objects = LiveManager(include_soft_deleted=True)

    def delete(self, *args, **kwargs):
        self.live = False
        self.save()

    def hard_delete(self):
        super(LiveModel, self).delete()

    class Meta:
        abstract = True


class LiveGeoModel(GeoModel):
    live = LiveField()

    objects = LiveGeoManager()
    all_objects = LiveGeoManager(include_soft_deleted=True)

    def delete(self, *args, **kwargs):
        self.live = False
        self.save()

    def hard_delete(self):
        super(LiveGeoModel, self).delete()

    class Meta:
        abstract = True
