from django.contrib.gis.db.models import Model as GeoModel

from ..fields import LiveField
from .managers import LiveGeoManager


class LiveGeoModel(GeoModel):
    """GeoModel support for soft-deleting using LiveField.

    LiveModel overrides Model.delete() to provide soft-deletion via
    a LiveField. `.delete()` updates `Model.live` to `True`. Normal
    deletion can performed usign `Model.hard_delete()`.
    """

    live = LiveField()

    objects = LiveGeoManager()
    all_objects = LiveGeoManager(include_soft_deleted=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.live = False
        self.save()

    def hard_delete(self):  # pylint: disable=super-on-old-class
        super(LiveGeoModel, self).delete()

    def undelete(self, *args, **kwargs):
        self.live = True
        self.save()
