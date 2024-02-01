from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config
from homeassistant.core import HomeAssistant
from .api.PrezziBenzina_client import prezzibenzina_client
from homeassistant.exceptions import ConfigEntryNotReady, ConfigEntryAuthFailed
from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, CONF_GAS_STATION_ID, PLATFORMS
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import logging
from homeassistant.helpers.update_coordinator import UpdateFailed
from datetime import timedelta

_LOGGER: logging.Logger = logging.getLogger(__package__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    if entry.options.get(CONF_SCAN_INTERVAL):
        update_interval = timedelta(seconds=entry.options[CONF_SCAN_INTERVAL])
    else:
        update_interval = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

    gas_station_id = entry.data.get(CONF_GAS_STATION_ID)


    coordinator = PrezziBenzinaDataUpdateCoordinator(hass, gas_station_id, update_interval=update_interval)
    await coordinator.async_config_entry_first_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    coordinator.platforms.extend(PLATFORMS)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


    return True


class PrezziBenzinaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, gas_station_id, update_interval: timedelta) -> None:
        """Initialize."""
        self._gas_station_id = gas_station_id
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)


    async def _async_update_data(self):
        """Update data via library."""
        try:
            return prezzibenzina_client.retrive_info(self._gas_station_id)
        except Exception as exception:
            _LOGGER.exception(exception)
            raise UpdateFailed() from exception