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

    @staticmethod
    def getattr(attribute_type):
        """Checks if the type has an attribute and parses it."""
        matching_attribute = re.match(r"^!(\w+):\w+$", attribute_type)
        return matching_attribute.group(1) if matching_attribute else None

    def grants(self, attribute_type):
        # Creates a regular expression in the following form:
        # ^(?=PERMITTED_ATTRIBUTES)(?:(?!FORBIDDEN_ATTRIBUTES)\w+(?::\w+)?)$
        # where the list of forbidden and permitted attributes is determined
        # by filtering the particular setting attributes by the "!" prefix.
        permit = r"|".join(filter(self.permitted, self.attributes))
        permit = r"\w+" if any(filter(self.getattr, self.attributes)) else permit
        forbid = r"|".join(map(self.normalize, filter(self.forbidden, self.attributes)))
        forbid = r"(?!" + forbid + r")" if forbid else ""
        regexp = r"^(?=" + permit + r")(?:" + forbid + r"\w+(?::\w+)?)$"

        # Regexp designed to match the permitted attributes.
        return re.match(regexp, attribute_type)


continents_codes = {
    'AF': ['AS'], 'AL': ['EU'], 'AQ': ['AN'], 'DZ': ['AF'], 'AS': ['OC'], 'AD': ['EU'], 'AO': ['AF'], 'AG': ['NA'],
    'AZ': ['EU', 'AS'], 'AR': ['SA'], 'AU': ['OC'], 'AT': ['EU'], 'BS': ['NA'], 'BH': ['AS'], 'BD': ['AS'],
    'AM': ['EU', 'AS'], 'BB': ['NA'], 'BE': ['EU'], 'BM': ['NA'], 'BT': ['AS'], 'BO': ['SA'], 'BA': ['EU'],
    'BW': ['AF'], 'BV': ['AN'], 'BR': ['SA'], 'BZ': ['NA'], 'IO': ['AS'], 'SB': ['OC'], 'VG': ['NA'], 'BN': ['AS'],
    'BG': ['EU'], 'MM': ['AS'], 'BI': ['AF'], 'BY': ['EU'], 'KH': ['AS'], 'CM': ['AF'], 'CA': ['NA'], 'CV': ['AF'],
    'KY': ['NA'], 'CF': ['AF'], 'LK': ['AS'], 'TD': ['AF'], 'CL': ['SA'], 'CN': ['AS'], 'TW': ['AS'], 'CX': ['AS'],
    'CC': ['AS'], 'CO': ['SA'], 'KM': ['AF'], 'YT': ['AF'], 'CG': ['AF'], 'CD': ['AF'], 'CK': ['OC'], 'CR': ['NA'],
    'HR': ['EU'], 'CU': ['NA'], 'CY': ['EU', 'AS'], 'CZ': ['EU'], 'BJ': ['AF'], 'DK': ['EU'], 'DM': ['NA'],
    'DO': ['NA'], 'EC': ['SA'], 'SV': ['NA'], 'GQ': ['AF'], 'ET': ['AF'], 'ER': ['AF'], 'EE': ['EU'], 'FO': ['EU'],
    'FK': ['SA'], 'GS': ['AN'], 'FJ': ['OC'], 'FI': ['EU'], 'AX': ['EU'], 'FR': ['EU'], 'GF': ['SA'], 'PF': ['OC'],
    'TF': ['AN'], 'DJ': ['AF'], 'GA': ['AF'], 'GE': ['EU', 'AS'], 'GM': ['AF'], 'PS': ['AS'], 'DE': ['EU'],
    'GH': ['AF'], 'GI': ['EU'], 'KI': ['OC'], 'GR': ['EU'], 'GL': ['NA'], 'GD': ['NA'], 'GP': ['NA'], 'GU': ['OC'],
    'GT': ['NA'], 'GN': ['AF'], 'GY': ['SA'], 'HT': ['NA'], 'HM': ['AN'], 'VA': ['EU'], 'HN': ['NA'], 'HK': ['AS'],
    'HU': ['EU'], 'IS': ['EU'], 'IN': ['AS'], 'ID': ['AS'], 'IR': ['AS'], 'IQ': ['AS'], 'IE': ['EU'], 'IL': ['AS'],
    'IT': ['EU'], 'CI': ['AF'], 'JM': ['NA'], 'JP': ['AS'], 'KZ': ['EU', 'AS'], 'JO': ['AS'], 'KE': ['AF'],
    'KP': ['AS'], 'KR': ['AS'], 'KW': ['AS'], 'KG': ['AS'], 'LA': ['AS'], 'LB': ['AS'], 'LS': ['AF'], 'LV': ['EU'],
    'LR': ['AF'], 'LY': ['AF'], 'LI': ['EU'], 'LT': ['EU'], 'LU': ['EU'], 'MO': ['AS'], 'MG': ['AF'], 'MW': ['AF'],
    'MY': ['AS'], 'MV': ['AS'], 'ML': ['AF'], 'MT': ['EU'], 'MQ': ['NA'], 'MR': ['AF'], 'MU': ['AF'], 'MX': ['NA'],
    'MC': ['EU'], 'MN': ['AS'], 'MD': ['EU'], 'ME': ['EU'], 'MS': ['NA'], 'MA': ['AF'], 'MZ': ['AF'], 'OM': ['AS'],
    'NA': ['AF'], 'NR': ['OC'], 'NP': ['AS'], 'NL': ['EU'], 'AN': ['NA'], 'CW': ['NA'], 'AW': ['NA'], 'SX': ['NA'],
    'BQ': ['NA'], 'NC': ['OC'], 'VU': ['OC'], 'NZ': ['OC'], 'NI': ['NA'], 'NE': ['AF'], 'NG': ['AF'], 'NU': ['OC'],
    'NF': ['OC'], 'NO': ['EU'], 'MP': ['OC'], 'UM': ['OC', 'NA'], 'FM': ['OC'], 'MH': ['OC'], 'PW': ['OC'],
    'PK': ['AS'], 'PA': ['NA'], 'PG': ['OC'], 'PY': ['SA'], 'PE': ['SA'], 'PH': ['AS'], 'PN': ['OC'], 'PL': ['EU'],
    'PT': ['EU'], 'GW': ['AF'], 'TL': ['AS'], 'PR': ['NA'], 'QA': ['AS'], 'RE': ['AF'], 'RO': ['EU'], 'RW': ['AF'],
    'RU': ['EU', 'AS'], 'BL': ['NA'], 'SH': ['AF'], 'KN': ['NA'], 'AI': ['NA'], 'LC': ['NA'], 'MF': ['NA'],
    'PM': ['NA'], 'VC': ['NA'], 'SM': ['EU'], 'ST': ['AF'], 'SA': ['AS'], 'SN': ['AF'], 'RS': ['EU'], 'SC': ['AF'],
    'SL': ['AF'], 'SG': ['AS'], 'SK': ['EU'], 'VN': ['AS'], 'SI': ['EU'], 'SO': ['AF'], 'ZA': ['AF'], 'ZW': ['AF'],
    'ES': ['EU'], 'SS': ['AF'], 'EH': ['AF'], 'SD': ['AF'], 'SR': ['SA'], 'SJ': ['EU'], 'SZ': ['AF'], 'SE': ['EU'],
    'CH': ['EU'], 'SY': ['AS'], 'TJ': ['AS'], 'TH': ['AS'], 'TG': ['AF'], 'TK': ['OC'], 'TO': ['OC'], 'TT': ['NA'],
    'AE': ['AS'], 'TN': ['AF'], 'TR': ['EU', 'AS'], 'TM': ['AS'], 'TC': ['NA'], 'TV': ['OC'], 'UG': ['AF'],
    'UA': ['EU'], 'MK': ['EU'], 'EG': ['AF'], 'GB': ['EU'], 'GG': ['EU'], 'JE': ['EU'], 'IM': ['EU'], 'TZ': ['AF'],
    'US': ['NA'], 'VI': ['NA'], 'BF': ['AF'], 'UY': ['SA'], 'UZ': ['AS'], 'VE': ['SA'], 'WF': ['OC'], 'WS': ['OC'],
    'YE': ['AS'], 'ZM': ['AF'], 'XX': ['OC'], 'XE': ['AS'], 'XD': ['AS'], 'XS': ['AS']
}
