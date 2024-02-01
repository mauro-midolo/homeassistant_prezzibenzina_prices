from homeassistant import config_entries
from .const import DOMAIN, CONF_GAS_STATION_ID
from api.PrezziBenzina_client import prezzibenzina_client

class PrezziBenzinaStatusFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Electrolux Status."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_GAS_STATION_ID]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_GAS_STATION_ID], data=user_input
                )
            else:
                self._errors["base"] = "gas_station_not_exists"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    
    async def _test_credentials(self, gas_station_id):
        """Return true if credentials is valid."""
        return prezzibenzina_client().id_exists(gas_station_id)
