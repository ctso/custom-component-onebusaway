"""Sensor platform for onebusaway."""
import logging

import async_timeout
import voluptuous as vol

from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    STATE_UNKNOWN,
    CONF_API_KEY,
    CONF_NAME,
    DEVICE_CLASS_TIMESTAMP,
)
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.util.dt import utc_from_timestamp
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

ICON = "mdi:bus"

CONF_ROUTE = "route"
CONF_STOP = "stop"

TIMEOUT = 10

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_STOP): cv.string,
        vol.Required(CONF_ROUTE): cv.string,
    }
)


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=unused-argument
    """Setup sensor platform."""

    async_add_entities([OneBusAwaySensor(hass, config)], True)


async def fetch_api(session, url):
    with async_timeout.timeout(TIMEOUT):
        resp = await session.get(url)
        body = await resp.json()

        return body


def from_epoch_ms(ts):
    return utc_from_timestamp(ts / 1000).isoformat()


class OneBusAwaySensor(Entity):
    """OneBusAway Sensor class."""

    def __init__(self, hass, config):
        self.hass = hass
        self.attr = {}
        self._state = STATE_UNKNOWN
        self._name = config.get(CONF_NAME)
        self._stop = config.get(CONF_STOP)
        self._route = config.get(CONF_ROUTE)
        self._api_key = config.get(CONF_API_KEY)

    async def async_update(self):
        """Update the sensor."""
        # TODO break out into client class
        api_url = (
            "http://api.pugetsound.onebusaway.org/api/where/"
            "arrivals-and-departures-for-stop/{}.json?key={}"
        )

        request_url = api_url.format(self._stop, self._api_key)
        _LOGGER.debug("Requesting %s", request_url)

        session = self.hass.helpers.aiohttp_client.async_get_clientsession()
        response = await fetch_api(session, request_url)

        if response["code"] != 200:
            _LOGGER.warn("Invalid response code from API: %s", response["code"])
            return

        departures = response["data"]["entry"]["arrivalsAndDepartures"]

        for departure in departures:
            # Filter down to the configured route
            if departure["routeId"] != self._route:
                continue

            # Ignore departures that passengers cannot use (maybe the bus is going back to the terminal)
            if not departure["departureEnabled"]:
                continue

            # Prefer predicted times, but fall back to schedule as necessary
            if departure["predictedArrivalTime"] > 0:
                self._state = from_epoch_ms(departure["predictedDepartureTime"])
            else:
                self._state = from_epoch_ms(departure["scheduledDepartureTime"])

            _LOGGER.debug("next departure is %s", self._state)
            break

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.attr

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_TIMESTAMP
