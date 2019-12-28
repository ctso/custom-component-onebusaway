# onebusaway

[![GitHub Activity][commits-badge]][commits]
[![hacs][hacs-badge]][hacs]

_Component to integrate with Puget Sound [OneBusAway][onebusaway]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show departures for a given bus stop and route.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `onebusaway`.
4. Download _all_ the files from the `custom_components/onebusaway/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Add configuration, see example below
7. Restart Home Assistant

## Example configuration.yaml

```yaml
sensor:
  - platform: onebusaway
    name: onebusaway_3rd_virginia_route_3
    api_key: YOUR_API_KEY
    stop: "1_600"
    route: "1_100173"
```

## Configuration options for `sensor` platform

Key | Type | Required | Description
-- | -- | -- | --
`api_key` | `string` | `True` | OneBusAway API Key
`route` | `string` | `True` | Route ID
`stop` | `string` | `True` | Stop ID

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[onebusaway]: http://pugetsound.onebusaway.org/
[commits]: https://github.com/ctso/custom-component-onebusaway/commits/master
[commits-badge]: https://img.shields.io/github/commit-activity/y/ctso/custom-component-onebusaway?style=flat-square
[hacs]: https://github.com/custom-components/hacs
[hacs-badge]: https://img.shields.io/badge/HACS-custom--component-orange.svg?style=flat-square