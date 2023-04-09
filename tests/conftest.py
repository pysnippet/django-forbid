from pathlib import Path

import pytest
from django.conf import settings
from django.http import HttpResponse


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


@pytest.fixture
def get_response():
    """A dummy view function."""

    def get_response_mock(_):
        return HttpResponse()

    return get_response_mock
