# Django Forbid <img src="https://github.com/pysnippet.png" align="right" height="64" />

Django app for forbidding access to some countries.

[![PyPI](https://img.shields.io/pypi/v/django-forbid.svg)](https://pypi.org/project/django-forbid/)
[![License](https://img.shields.io/pypi/l/django-forbid.svg)](https://github.com/pysnippet/django-forbid/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)

[//]: # ([![Tests]&#40;https://github.com/pysnippet/django-forbid/actions/workflows/tests.yml/badge.svg&#41;]&#40;https://github.com/pysnippet/django-forbid/actions/workflows/tests.yml&#41;)

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

## Contribute

Any contribution is welcome. If you have any ideas or suggestions, feel free to open an issue or a pull request. And
don't forget to add tests for your changes.

## License

Copyright (C) 2023 Artyom Vancyan. [MIT](https://github.com/pysnippet/django-forbid/blob/master/LICENSE)
