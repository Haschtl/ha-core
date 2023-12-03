"""Crescontrol number entities.

Can be:
- out-X:voltage
"""
import logging
from typing import Any

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescience.crescontrol import CresControl
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity, UpdateError
from .helper import path2number_device_class, path2number_range

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static Number entities for entry."""
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    sensors = []
    for entity_key, config in STATIC_CRESCONTROL_FEATURES["entities"].items():
        if config["type"] == Platform.NUMBER:
            # and entity_key in extra_sensors:
            sensor = CresControlNumber(device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlNumber(CresControlEntity, NumberEntity):
    """CresControl Number Entity."""

    def __init__(
        self, device: CresControl, path: str, config: EntityDefinition
    ) -> None:
        """Create new CresControl Number Entity."""
        super().__init__(device, path, config)
        self._attr_native_value = 0
        self._attr_device_class = path2number_device_class(path)
        # self._attr_entity_registry_enabled_default = path2default_enabled(path)
        # self._attr_icon = path2icon(path)
        numberRange = path2number_range(path)
        self._attr_native_min_value = numberRange["min"]
        self._attr_native_max_value = numberRange["max"]
        self._attr_native_step = numberRange["step"]

    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.send(f"voltage={value}")

    def update_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            self._attr_native_value = float(value)
        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    def pull_custom(self) -> bool:
        """Request the entity data from the device, if entity-type is custom."""
        if self.path in ("out-a", "out-b", "out-c", "out-d", "out-e", "out-f"):
            return True
            # self.device.send(
            #     f"{self.path}:meta;{self.path}:enabled;{self.path}:pwm-enabled;{self.path}:pwm-frequency;{self.path}:threshold;{self.path}:calib-offset;{self.path}:calib-factor"
            # )
        return False

    def update_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        if path.startswith(self.path + ":"):
            if path == f"{self.path}:voltage":
                self.update_main_value(value)
                return True
        return False
