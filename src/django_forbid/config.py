from django.conf import settings


class Settings:
    """A helper class to access settings in a more convenient way."""

    @classmethod
    def _get(cls, item):
        result = getattr(settings, "DJANGO_FORBID", {})
        for attr in item.split("."):
            result = result[attr]
        return result

    @classmethod
    def has(cls, item):
        try:
            cls._get(item)
            return True
        except KeyError:
            return False

    @classmethod
    def get(cls, item, default=None):
        try:
            return cls._get(item)
        except KeyError:
            return default
