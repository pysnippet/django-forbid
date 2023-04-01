# Django Forbid <img src="https://github.com/pysnippet.png" align="right" height="64" />

Django app for forbidding access to some countries.

[![PyPI](https://img.shields.io/pypi/v/django-forbid.svg)](https://pypi.org/project/django-forbid/)
[![Django](https://img.shields.io/badge/django-%3E%3D2.1-blue.svg)](https://pypi.org/project/django-forbid/)
[![Python](https://img.shields.io/pypi/pyversions/django-forbid.svg)](https://pypi.org/project/django-forbid/)
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
And there are four setting variables for describing any of your specific needs:

- `WHITELIST_COUNTRIES` and `WHITELIST_TERRITORIES` - Correspondingly, the list of countries and territories that are
  allowed to access the site.
- `FORBIDDEN_COUNTRIES` and `FORBIDDEN_TERRITORIES` - Correspondingly, the list of countries and territories that are
  forbidden to access the site.

Forbidden countries and territories have a higher priority than allowed ones. If a country or territory is in both
lists, then the user will be forbidden. And if the user is not allowed to access the resource, it will be redirected to
the `FORBIDDEN_URL` page if the variable is set in your Django project's settings.

```python
# Only US, GB, and EU countries are allowed to access the site.
WHITELIST_COUNTRIES = ['US', 'GB']
WHITELIST_TERRITORIES = ['EU']
```

Needs can be different, so you can use any combination of these variables to describe your special needs.

```python
# Forbid access for African countries and Russia, Belarus, and North Korea.
FORBIDDEN_COUNTRIES = ['RU', 'BY', 'KP']
FORBIDDEN_TERRITORIES = ['AF']
```

The available ISO 3166 alpha-2 country codes are listed in [here](https://www.iban.com/country-codes). And the available
ISO continent codes are: `AF` - Africa, `AN` - Antarctica, `AS` - Asia, `EU` - Europe, `NA` - North America, `OC` -
Oceania and `SA` - South America.

Without additional configuration, the middleware will check the user's access on every request. This can slow down the
site. To avoid this, you can use the `FORBID_TIMEOUT` variable to set the cache timeout in seconds. When the timeout
expires, the middleware will check the user's access again.

```python
# Check the user's access every 10 minutes.
FORBID_TIMEOUT = 60 * 10
```

## Contribute

Any contribution is welcome. If you have any ideas or suggestions, feel free to open an issue or a pull request. And
don't forget to add tests for your changes.

## License

Copyright (C) 2023 Artyom Vancyan. [MIT](https://github.com/pysnippet/django-forbid/blob/master/LICENSE)
