# Configuration

The following configurations for the application are required and done in the project's **settings.py** file and include
the following steps.

## Installed Apps

Add the `django_forbid.apps.ForbidConfig` to your `INSTALLED_APPS` for initializing the app and using its components.

```python
INSTALLED_APPS = [
    ...,  # other apps
    'django_forbid.apps.ForbidConfig',
]
```

## Middleware

Add the `django_forbid.middleware.ForbidMiddleware` to the `MIDDLEWARE` list to enable its features to control access to
the requested resource based on the provided settings.

```python
MIDDLEWARE = [
    ...,  # other middlewares
    'django_forbid.middleware.ForbidMiddleware',
]
```

## GeoIP2

Configuring the `GEOIP_PATH` variable is important. This variable should contain the path to the GeoLite2 database file.
You can [download](https://dev.maxmind.com/geoip/geoip2/geolite2/) the database from MaxMind's website.
The `GeoLite2-City.mmdb` file is enough for this application. The `GEOIP_PATH` variable should be set to the directory
containing the database file.

```python
GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')
```

Also, check out the official
Django [documentation](https://docs.djangoproject.com/en/2.1/ref/contrib/gis/geoip2/#settings) for proper and detailed
configuration.
