"""Crescontrol binary-sensor entities.

Can be:
- wifi:connected
"""
import logging
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescience.crescontrol import CresControl
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity, UpdateError
from .helper import path2binary_sensor_device_class

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static BinarySensor entities for entry."""
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    sensors = []
    for entity_key, config in STATIC_CRESCONTROL_FEATURES["entities"].items():
        if config["type"] == Platform.BINARY_SENSOR:
            sensor = CresControlBinarySensor(hass, device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlBinarySensor(CresControlEntity, BinarySensorEntity):
    """CresControl Binary Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device: CresControl,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Binary Entity."""
        super().__init__(hass, device, path, config)

        if path == "connected":
            self._device.set_connected_entity(self)
        else:
            self._attr_state_class = "measurement"
            self._attr_device_class = path2binary_sensor_device_class(path)

    def update_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            self._attr_is_on = bool(value)
        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    def pull_custom(self) -> bool:
        """No pulling for custom binary sensors."""
        return False

    def update_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        if self.path == "connected":
            # self._attr_native_value = "connected"
            return False
        if path.startswith(self.path):
            if path == f"{self.path}":
                self.update_main_value(value)
                return True
        return False
