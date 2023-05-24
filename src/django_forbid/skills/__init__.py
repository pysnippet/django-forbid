import re

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


class Access:
    """A helper class to check if a user has access to a resource."""

    def __init__(self, attributes):
        self.attributes = attributes

    @staticmethod
    def normalize(attribute_type):
        """Removes the "!" prefix."""
        return attribute_type[1:]

    @staticmethod
    def forbidden(attribute_type):
        """Checks if the type is forbidden."""
        return attribute_type.startswith("!")

    @classmethod
    def permitted(cls, attribute_type):
        """Checks if the type is permitted."""
        return not cls.forbidden(attribute_type)

    def grants(self, attribute_type):
        # Creates a regular expression in the following form:
        # ^(?=PERMITTED_ATTRIBUTES)(?:(?!FORBIDDEN_ATTRIBUTES)\w)+$
        # where the list of forbidden and permitted attributes are
        # filtered from the ATTRIBUTES setting by the "!" prefix.
        permit = r"|".join(filter(self.permitted, self.attributes))
        forbid = r"|".join(map(self.normalize, filter(self.forbidden, self.attributes)))
        forbid = r"(?!" + forbid + r")" if forbid else ""
        regexp = r"^(?=" + permit + r")(?:" + forbid + r"\w)+$"

        # Regexp designed to match the permitted attributes.
        return re.match(regexp, attribute_type)
