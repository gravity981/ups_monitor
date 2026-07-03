from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfElectricPotential
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        X1205Battery(coordinator, entry.entry_id),
        X1205Voltage(coordinator, entry.entry_id),
        X1205Charging(coordinator, entry.entry_id),
    ])


class X1205Battery(CoordinatorEntity, SensorEntity):
    _attr_name = "UPS Battery"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_battery"

    @property
    def native_value(self):
        return self.coordinator.data["battery"]


class X1205Voltage(CoordinatorEntity, SensorEntity):
    _attr_name = "UPS Voltage"
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.MILLIVOLT
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_voltage"

    @property
    def native_value(self):
        return self.coordinator.data["voltage"]


class X1205Charging(CoordinatorEntity, SensorEntity):
    _attr_name = "UPS Charging"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["charging", "discharging"]

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_charging"

    @property
    def native_value(self):
        return "charging" if self.coordinator.data["charging"] else "discharging"
