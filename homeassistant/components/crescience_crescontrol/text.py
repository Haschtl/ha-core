"""Crescontrol text entities.

Can be:
- out-X:meta
"""
import logging
from typing import Any

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity, UpdateError
from .helper import path2text_pattern

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static Text entities for entry."""
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    sensors = []
    for entity_key, config in STATIC_CRESCONTROL_FEATURES["entities"].items():
        if config["type"] == Platform.TEXT:
            sensor = CresControlText(hass, device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlText(CresControlEntity, TextEntity):
    """CresControl Text Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Text Entity."""
        super().__init__(hass, device, path, config)

        # self._attr_state_class = "measurement"
        # self._attr_device_class = path2sensor_device_class(path)
        # self._attr_entity_registry_enabled_default = not config["hidden"]
        # self._attr_entity_registry_enabled_default = path2default_enabled(path)
        # self._attr_native_unit_of_measurement = path2unit(path)
        # self._attr_icon = path2icon(path)
        self._attr_native_mode = "text"
        self._attr_pattern = path2text_pattern(path)

    def set_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            self._attr_native_value = str(value)
        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    def set_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        if path.startswith(self.path):
            if path == f"{self.path}":
                self.set_main_value(value)
                return True
        return False
