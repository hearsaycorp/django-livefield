from django.db import models

from .live_field import LiveField


class LiveModel(models.Model):
    """Model support for soft-deleting using LiveField

    LiveModel overrides Model.delete() to provide soft-deletion via
    a LiveField. `.delete()` updates `Model.live` to `True`. Normal
    deletion can performed usign `Model.hard_delete()`.
    """

    live = LiveField()

    class Meta:
        abstract = True

    def delete(self):
        self.soft_delete()

    def hard_delete(self):
        super(LiveModel, self).delete()

    def soft_delete(self):
        self.live = False
        self.save()
