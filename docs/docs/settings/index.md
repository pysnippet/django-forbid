# Settings Introduction

After connecting the Django Forbid to your project, you can define the set of desired zones to be forbidden or allowed.
All you need is to set the `DJANGO_FORBID` variable in your project's settings. It should be a dictionary with the
following keys:

- `DEVICES` - list of devices to permit or forbid access to
- `COUNTRIES` - list of countries to permit or forbid access to
- `TERRITORIES` - list of territories to permit or forbid access to
- `OPTIONS` - a dictionary for additional settings
    - `ACTION` - whether to `PERMIT` or `FORBID` access to the listed zones (default is `FORBID`)
    - `PERIOD` - time in seconds to check for access again, 0 means on each request
    - `VPN` - use VPN detection and forbid access to VPN users
    - `URL` - set of URLs to redirect to when the user is located in a forbidden country or using a VPN
        - `FORBIDDEN_LOC` - the URL to redirect to when the user is located in a forbidden country
        - `FORBIDDEN_VPN` - the URL to redirect to when the user is using a VPN
        - `FORBIDDEN_KIT` - the URL to redirect to when the user is using a forbidden device

Unlike the `COUNTRIES` and `TERRITORIES`, where the middleware decides whether to permit or forbid access based on the
given `ACTION` value, the `DEVICES` list accepts device types where the names starting with `!` are forbidden. This is
done to make it possible to make them all mix together.
