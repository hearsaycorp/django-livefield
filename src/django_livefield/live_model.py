from django.db import models

from django.contrib.gis.db.models import Model as GeoModel

from .live_field import LiveField
from .live_manager import LiveManager, LiveGeoManager


class LiveModel(models.Model):
    """Model support for soft-deleting using LiveField

    LiveModel overrides Model.delete() to provide soft-deletion via
    a LiveField. `.delete()` updates `Model.live` to `True`. Normal
    deletion can performed usign `Model.hard_delete()`.
    """

    live = LiveField()

    objects = LiveManager()
    all_objects = LiveManager(include_soft_deleted=True)

    class Meta:
        abstract = True

    def delete(self):
        self.soft_delete()

    def hard_delete(self):
        super(LiveModel, self).delete()

    def soft_delete(self):
        self.live = False
        self.save()


class LiveGeoModel(GeoModel):
    """GeoModel support for soft-deleting using LiveField

    LiveModel overrides Model.delete() to provide soft-deletion via
    a LiveField. `.delete()` updates `Model.live` to `True`. Normal
    deletion can performed usign `Model.hard_delete()`.
    """

    live = LiveField()

    objects = LiveGeoManager()
    all_objects = LiveGeoManager(include_soft_deleted=True)

    def delete(self, *args, **kwargs):
        self.live = False
        self.save()

    def hard_delete(self):
        super(LiveGeoModel, self).delete()

    def undelete(self, *args, **kwargs):
        self.live = True
        self.save()

    class Meta:
        abstract = True
