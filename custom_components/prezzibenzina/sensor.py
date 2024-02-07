from typing import cast

from .api import ApplianceSensor
from .const import DOMAIN
from .const import SENSOR
from .api.PrezziBenzina import PrezziBenzina
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from . import PrezziBenzinaDataUpdateCoordinator
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CURRENCY_EURO

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator: PrezziBenzinaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    data: PrezziBenzina = coordinator.data


    for value in PrezziBenzina.get_values:
        async_add_devices(PrezziBenzinaStatusSensor(coordinator, entry, value['fuel'], value['service']))




class PrezziBenzinaStatusEntity(CoordinatorEntity):
    def __init__(self, coordinator: PrezziBenzinaDataUpdateCoordinator, config_entry, fuel, service):
        super().__init__(coordinator)
        self.api = coordinator.api
        self.config_entry = config_entry
        self.fuel = fuel
        self.service = service
        self._unit_of_measurement = CURRENCY_EURO
        self._device_class = "COST"
        self._entity_category = "EXPENSE"

    @property
    def name(self):
        """Return the name of the sensor."""
        data: PrezziBenzina = self.coordinator.data
        return data.get_name


    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        data: PrezziBenzina = self.coordinator.data
        return f"{self.config_entry.entry_id}-{self.fuel}-{self.service}"

    @property
    def device_info(self):
        data: PrezziBenzina = self.coordinator.data
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": data.get_name,
            "model": data.get_street
        }
        
    @property
    def get_value(self):
        data: PrezziBenzina = self.coordinator.data
        filtered_data = filter(lambda x: x['fuel'] == self.fuel and x['service'] == self.service, data)
        return list(filtered_data)[0]
    
    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def device_class(self):
        return self._device_class

    @property
    def entity_category(self):
        return self._entity_category

    
class PrezziBenzinaStatusSensor(PrezziBenzinaStatusEntity, SensorEntity):
    """Electrolux Status Sensor class."""
    
    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.get_value()['price']
