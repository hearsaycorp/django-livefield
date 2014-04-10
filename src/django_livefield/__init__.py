from .fields import LiveField  # noqa
from .managers import LiveManager, LiveGeoManager  # noqa
from .querysets import LiveQuerySet, LiveGeoQuerySet  # noqa
from .models import LiveModel, LiveGeoModel


__all__ = (
    # Standard Django
    'LiveField',
    'LiveManager',
    'LiveQuerySet',
    'LiveModel',
    # GeoDjango
    'LiveGeoField',
    'LiveGeoManager',
    'LiveGeoQuerySet',
    'LiveGeoModel',
)


__version__ = 'unknown'
try:
    __version__ = __import__('pkg_resources').get_distribution('django_livefield').version
except Exception as e:
    pass
