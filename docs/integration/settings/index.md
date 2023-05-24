# Settings Introduction

After connecting the Django Forbid to your project, you can define the set of desired zones to be forbidden or allowed.
All you need is to set the `DJANGO_FORBID` variable in your project's settings. It should be a dictionary with the
following keys.

## Setting Keys

- `DEVICES` - list of devices to permit or forbid access to
- `COUNTRIES` - list of countries to permit or forbid access to
- `TERRITORIES` - list of territories to permit or forbid access to
- `OPTIONS` - a dictionary for additional settings
    - `VPN` - use VPN detection and forbid access to VPN users
    - `URL` - set of URLs to redirect to when the user is located in a forbidden country or using a VPN
        - `FORBIDDEN_LOC` - the URL to redirect to when the user is located in a forbidden geolocation
        - `FORBIDDEN_NET` - the URL to redirect to when the user is using a forbidden network (VPN)
        - `FORBIDDEN_DEV` - the URL to redirect to when the user is using a forbidden device

These variables are all covered in more detail at the [next page](./variables.md).

## Initialization

To initialize the Django Forbid, you need to define the `DJANGO_FORBID` variable. Here is an example of how it can be
done.

```python
DJANGO_FORBID = {
    'DEVICES': ['desktop', 'smartphone', 'console', 'tablet', 'tv'],
    'COUNTRIES': ['US', 'GB'],
    'TERRITORIES': ['EU'],
    'OPTIONS': {
        'VPN': True,
        'URL': {
            'FORBIDDEN_LOC': 'forbidden_location',
            'FORBIDDEN_NET': 'forbidden_network',
            'FORBIDDEN_DEV': 'forbidden_device',
        },
    },
}
```

In this example, the Django Forbid will permit access to users using the listed devices and forbid entry to users
worldwide except for the US, UK, and EU countries. It will also forbid access to the users who use VPN to lie about
their geolocation. The settings also define the URLs to redirect to when access is forbidden.
