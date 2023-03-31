from django.conf import settings
from pathlib import Path


def pytest_configure():
    settings.configure(
        INSTALLED_APPS=[
            "django_forbid.apps.ForbidConfig"
        ],
        MIDDLEWARE=[
            "django_forbid.middleware.ForbidMiddleware"
        ],
        # The `pathlib.Path` support was added after Django 3.0.
        GEOIP_PATH=(Path(__file__).parent / "geoip").as_posix(),
    )
