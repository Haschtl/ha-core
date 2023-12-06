"""Crescontrol date entities.

Can be:
- time:date
"""
from datetime import datetime
import logging
from typing import Any

from homeassistant.components.date import DateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES
from .crescontrol_entity import CresControlEntity, UpdateError

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static Date entities for entry."""
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    sensors = []
    for entity_key, config in STATIC_CRESCONTROL_FEATURES["entities"].items():
        if config["type"] == Platform.DATE:
            sensor = CresControlDate(hass, device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlDate(CresControlEntity, DateEntity):
    """CresControl Date Entity."""

    # def __init__(
    #     self, device: CresControl, path: str, config: EntityDefinition
    # ) -> None:
    #     """Create new CresControl Date Entity."""
    #     super().__init__(device, path, config)

    def set_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            # dateParts = (
            #     str(value)
            #     .replace("h", "")
            #     .replace("m", "")
            #     .replace("s", "")
            #     .replace('"', "")
            #     .split(":")
            # )
            # self._attr_native_value = date(
            #     int(timeParts[0]), int(timeParts[1]), int(timeParts[2])
            # )
            # self._attr_native_value = parser.parse(str(value)).date()
            self._attr_native_value = datetime.strptime(
                cresStr(value), "%A, %d. %B %Y"
            ).date()
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


def cresStr(value: Any):
    """Parse string from CresProtocol."""
    value = str(value)
    if value.startswith('"'):
        return value[1:-1]

    return value
