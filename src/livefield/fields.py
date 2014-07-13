from django.db import models


class LiveField(models.NullBooleanField):
    """Support uniqueness constraints and soft-deletion.

    Similar to a BooleanField, but stores False as NULL. This lets us use
    database constraints to enforce uniqueness of live objects but still allow
    many duplicate dead objects (treating each NULL as a unique snowflake
    follows the ANSI SQL standard, and works in both MySQL and Postgres).

    """
    description = u'Soft-deletion status'
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(LiveField, self).__init__(default=True, null=True)

    def get_prep_value(self, value):
        # Convert in-Python value to value we'll store in DB
        if value:
            return super(LiveField, self).get_prep_value(True)
        return None

    def to_python(self, value):
        # Somewhat misleading name, since this type coercion also occurs when
        # assigning a value to the field in Python.
        return bool(value)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type == 'exact' and not value:
            msg = u"%(model)s doesn't support filters or excludes with %(field)s=False. Try using %(field)s=None."
            raise TypeError(msg % {'model': self.model.__name__, 'field': self.name})
        return super(LiveField, self).get_prep_lookup(lookup_type, value)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^livefield.LiveField'])
except ImportError:
    pass
