# Django Forbid

Django Forbid aims to make website access managed and secure for the maintainers. It provides a middleware to grant or
deny user access based on device and/or location. It also supports VPN detection for banning users who want to lie about
their country and geolocation. Also, users can use only the VPN detection feature or disable it.

## Installation

This package requires Python 3.6 or newer and Django 2.1 or newer versions.

```shell
python -m pip install django-forbid
```

## Upgrade

Make sure you are using the latest version of Django Forbid for avoiding bugs and getting new features and best
performance. You can check the latest version on the [PyPI page](https://pypi.org/project/django-forbid/).

```shell
python -m pip install --upgrade django-forbid
```

## Dependencies

Django Forbid depends on the following packages.

- [django](https://github.com/django/django)
- [geoip2](https://github.com/maxmind/GeoIP2-python)
- [device_detector](https://github.com/thinkwelltwd/device_detector)
