# Django Forbid <img src="https://github.com/pysnippet.png" align="right" height="64" />

Django app for forbidding access to some countries.

[![PyPI](https://img.shields.io/pypi/v/django-forbid.svg)](https://pypi.org/project/django-forbid/)
[![Python](https://img.shields.io/pypi/pyversions/django-forbid.svg?logoColor=white)](https://pypi.org/project/django-forbid/)
[![Django](https://img.shields.io/pypi/djversions/django-forbid.svg?color=0C4B33&label=django)](https://pypi.org/project/django-forbid/)
[![License](https://img.shields.io/pypi/l/django-forbid.svg)](https://github.com/pysnippet/django-forbid/blob/master/LICENSE)
[![Tests](https://github.com/pysnippet/django-forbid/actions/workflows/tests.yml/badge.svg)](https://github.com/pysnippet/django-forbid/actions/workflows/tests.yml)

## Install

```shell
python -m pip install django-forbid
```

## Configuration

Add the `django_forbid.apps.ForbidConfig` to your `INSTALLED_APPS` in your Django project's **settings.py** file.

```python
INSTALLED_APPS = [
    ...,  # other apps
    'django_forbid.apps.ForbidConfig',
]
```

Also, add the `django_forbid.middleware.ForbidMiddleware` to the `MIDDLEWARE` list of the project.

```python
MIDDLEWARE = [
    ...,  # other middlewares
    'django_forbid.middleware.ForbidMiddleware',
]
```

Configuring the `GEOIP_PATH` variable in your project's settings is important. This variable should contain the path to
the GeoLite2 database file. You should [download](https://dev.maxmind.com/geoip/geoip2/geolite2/) the database and
follow the Django [documentation](https://docs.djangoproject.com/en/2.1/ref/contrib/gis/geoip2/#settings) for proper
configuration.

## Usage

After connecting the Django Forbid to your project, you can define the set of desired zones to be forbidden or allowed.
All you need is to set the `DJANGO_FORBID` variable in your project's settings. It should be a dictionary with the
following keys:

- `COUNTRIES` - list of countries to permit or forbid access to
- `TERRITORIES` - list of territories to permit or forbid access to
- `OPTIONS` - a dictionary for additional settings
  - `ACTION` - whether to `PERMIT` or `FORBID` access to the listed zones (default is `FORBID`)
  - `PERIOD` - time in seconds to check for access again, 0 means on each request
  - `VPN` - use VPN detection and forbid access to VPN users
  - `URL` - set of URLs to redirect to when the user is located in a forbidden country or using a VPN
      - `FORBIDDEN_LOC` - the URL to redirect to when the user is located in a forbidden country
      - `FORBIDDEN_VPN` - the URL to redirect to when the user is using a VPN

```python
DJANGO_FORBID = {
    'COUNTRIES': ['US', 'GB'],
    'TERRITORIES': ['EU'],
    'OPTIONS': {
        'ACTION': 'PERMIT',
        'PERIOD': 300,
        'VPN': True,
        'URL': {
            'FORBIDDEN_LOC': 'forbidden_country',
            'FORBIDDEN_VPN': 'forbidden_network',
        },
    },
}
```

The available ISO 3166 alpha-2 country codes are listed in [here](https://www.iban.com/country-codes). And the available
ISO continent codes are: `AF` - Africa, `AN` - Antarctica, `AS` - Asia, `EU` - Europe, `NA` - North America, `OC` -
Oceania and `SA` - South America.

_None of the settings are required. If you don't specify any settings, the middleware will not do anything._

## Contribute

Any contribution is welcome. If you have any ideas or suggestions, feel free to open an issue or a pull request. And
don't forget to add tests for your changes.

## License

Copyright (C) 2023 Artyom Vancyan. [MIT](https://github.com/pysnippet/django-forbid/blob/master/LICENSE)
