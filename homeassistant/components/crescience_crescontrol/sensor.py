"""Crescontrol sensor entities.

Can be:
- in-a
- in-b
- extensions:XXX-XXX:XXX
"""
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescience.crescontrol import CresControl
from .crescience.helper import represents_number
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity, UpdateError
from .helper import path2sensor_device_class, path2unit

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static Sensor entities for entry."""
    assert hass is not None
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    sensors = []
    for entity_key, config in STATIC_CRESCONTROL_FEATURES["entities"].items():
        if config["type"] == Platform.SENSOR:
            # and entity_key in extra_sensors:
            sensor = CresControlSensor(hass, device, entity_key, config)
            # sensor.hass = hass
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlSensor(CresControlEntity, SensorEntity):
    """CresControl Sensor Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device: CresControl,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Sensor Entity."""
        super().__init__(hass, device, path, config)
        self._attr_state_class = config["sensor_class"]
        self._attr_device_class = path2sensor_device_class(path)
        # self._attr_entity_registry_enabled_default = not config["hidden"]
        # self._attr_entity_registry_enabled_default = path2default_enabled(path)
        self._attr_native_unit_of_measurement = path2unit(path)
        # self._attr_icon = path2icon(path)

    def update_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            if represents_number(value):
                self._attr_native_value = float(value)
            else:
                self._attr_native_value = str(value)

        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    def pull_custom(self) -> bool:
        """Request the entity data from the device, if entity-type is custom."""
        if self.path in ("in-a", "in-b"):
            return True
            # self._device.send(
            #     f"{self.path}:meta;{self.path}:calib-offset;{self.path}:calib-factor"
            # )
        return False

    def update_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        if self.path == "connection_status":
            # self._attr_native_value = "connected"
            return False
        # if path == self.path:
        #     self.update_main_value(value)
        #     return True
        if path.startswith(self.path + ":"):
            if path == f"{self.path}:voltage":
                self.update_main_value(value)
                return True
            # for sub_path in ("meta", "calib-offset", "calib-factor"):
            #     if path == f"{self.path}:{sub_path}":
            #         self._attr_extra_state_attributes[sub_path] = value
            #         return True
        return False
