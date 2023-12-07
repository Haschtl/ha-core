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
            sensor = CresControlNumber(hass, device, entity_key, config)
            sensors.append(sensor)
    # await hass.async_add_executor_job(create_library_sensors)
    async_add_entities(sensors)


class CresControlNumber(CresControlEntity, NumberEntity):
    """CresControl Number Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Number Entity."""
        super().__init__(hass, device, path, config)
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
        if self._config["variant"] == "simple":
            self.send(f"={value}", True)
        else:
            self.set_native_value_custom(value)

    def set_native_value_custom(self, value: float) -> None:
        """Update the current value for custom entities."""
        if self.path in ("out-a", "out-b", "out-c", "out-d", "out-e", "out-f"):
            self.send(f"voltage={value}", True)

    def set_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            self._attr_native_value = float(value)
        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    def update_custom(self) -> bool:
        """Request the entity data from the device, if entity-type is custom."""
        if self.path in ("out-a", "out-b", "out-c", "out-d", "out-e", "out-f"):
            self.hass.add_job(self._device.send(f"{self.path}:voltage"))
            return True
        return False

    async def set_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        if path.startswith(self.path + ":"):
            if path == f"{self.path}:voltage":
                self.set_main_value(value)
                return True
        return False
