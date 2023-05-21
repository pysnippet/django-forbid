---
outline: deep
---

# Setting Variables

None of the settings are required. The Django Forbid will not be initialized if you don't define them. You can enable
Django Forbid features by setting the corresponding variables for the desired features.

## Devices

- Key: `DEVICES`
- Type: `list`
- Default: `[]`

The list of devices to permit or forbid access to. The list accepts device types where the names starting with the `!`
prefix are forbidden. This is done to make it possible to make `DEVICES`, `COUNTRIES`, and `TERRITORIES` mix together.

The list of available device types are:

- `smartphone` - all types of modern phones with innovative capabilities like iPhone, Android and Windows phones
- `peripheral` - refers to all hardware components that are attached to a computer like Printers, Scanners, Webcams, etc
- `wearable` - common types of wearable technology include smartwatches and smartglasses
- `phablet` - a smartphone having a larger screen - a combination of a phone and a tablet
- `console` - game consoles like PlayStation, Xbox, etc
- `display` - smart displays like Google Nest Hub, Amazon Echo Show, etc
- `speaker` - smart speakers like Google Assistant, Siri, Alexa, etc
- `desktop` - desktop and laptop computers
- `tablet` - refers to all types of tablets
- `camera` - refers to cameras that are not peripheral - including professional cameras with internet access, etc
- `player` - a portable media players like iPod, Sony Walkman, Creative Zen, etc
- `phone` - refers to all types of ordinary phones
- `car` - refers to a car browser
- `tv` - refers to TVs having internet access

## Countries

- Key: `COUNTRIES`
- Type: `list`
- Default: `[]`

The list of countries to permit or forbid access to. Countries are defined by their ISO 3166 alpha-2 codes, and the list
of all codes can be found [here](https://www.iban.com/country-codes).

## Territories

- Key: `TERRITORIES`
- Type: `list`
- Default: `[]`

The list of territories to permit or forbid access to. As countries, territories are also defined by their ISO 3166
alpha-2 codes, and the list of available continent codes (territories) are:

- `AF` - Africa
- `AN` - Antarctica
- `AS` - Asia
- `EU` - Europe
- `NA` - North America
- `OC` - Oceania
- `SA` - South America

## Options

- Key: `OPTIONS`
- Type: `dict`

The `OPTIONS` are secondary settings for enabling additional features and customizing primary settings behavior. The
available options are: `ACTION`, `PERIOD`, `VPN` and `URL`.

### Action

- Key: `ACTION`
- Type: `str`
- Default: `FORBID`

Unlike the `DEVICES` list, where the middleware decides whether to permit or forbid access based on the `!` prefix,
the `COUNTRIES` and `TERRITORIES` use the `ACTION` variable that defines the action that needs to be performed for the
users from the listed countries or territories. Possible values are `FORBID` and `PERMIT`.

### Period

- Key: `PERIOD`
- Type: `int`
- Default: `0`

The `PERIOD` variable defines the period of time in seconds for the next access check to the requested resource. It is
optimal to set this when VPN detection is enabled so that users will not be disgusted by frequent redirections - with
the default value, it will check for VPN for each done request.

### VPN

- Key: `VPN`
- Type: `bool`
- Default: `False`

The `VPN` variable defines whether to enable VPN detection or not. If enabled, the Django Forbid will check if the
requester uses a VPN and redirect the user to the specified URL. It is optimal to enable this option with `COUNTRIES`
and `TERRITORIES` to make sure users cannot cheat the rules by using virtual private networks. Also, you can use this
feature without specifying any location-defining variables and check only for the VPN.

### URL

- Key: `URL`
- Type: `dict`
- Default: `{}`

The `URL` variable defines the set of URLs to redirect to when Django Forbid forbids the user to access the requested
resource.

#### Forbidden Location

- Key: `FORBIDDEN_LOC`
- Type: `str`
- Default: `''`

This URL is used when the user is located in the forbidden country or territory. If not specified, the user will see
the default Django 403 page. The URL can be absolute or relative.

#### Forbidden Network

- Key: `FORBIDDEN_VPN`
- Type: `str`
- Default: `''`

This URL is used when the user is using a virtual private network (VPN). If not specified, the user will see the default
Django 403 page. The URL can be absolute or relative.

#### Forbidden Device

- Key: `FORBIDDEN_KIT`
- Type: `str`
- Default: `''`

This URL is used when the user is using a forbidden device. If not specified, the user will see the default Django 403
page. The URL can be absolute or relative.
