"""Crescontrol time entities.

Can be:
- time:daytime

"""
from datetime import time
import logging
from typing import Any

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity, UpdateError

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static Time entities for entry."""
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    sensors = []
    for entity_key, config in STATIC_CRESCONTROL_FEATURES["entities"].items():
        if config["type"] == Platform.TIME:
            # and entity_key in extra_sensors:
            sensor = CresControlTime(hass, device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlTime(CresControlEntity, TimeEntity):
    """CresControl Time Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Time Entity."""
        super().__init__(hass, device, path, config)
        self._attr_native_value = time(0, 0, 0)

    def set_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            timeParts = (
                str(value)
                .replace("d", "")
                .replace("h", "")
                .replace("m", "")
                .replace("s", "")
                .replace('"', "")
                .split(":")
            )
            if len(timeParts) == 4:
                timeParts = timeParts[1:]
            self._attr_native_value = time(
                int(timeParts[0]), int(timeParts[1]), int(timeParts[2])
            )
        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    async def set_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        return False
