"""Crescontrol select entities."""
import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescience.crescontrol import CresControl
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity, UpdateError
from .helper import path2select_options

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static Select entities for entry."""
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    sensors = []
    for entity_key, config in STATIC_CRESCONTROL_FEATURES["entities"].items():
        if config["type"] == Platform.SELECT:
            sensor = CresControlSelect(device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlSelect(CresControlEntity, SelectEntity):
    """CresControl Select Entity."""

    def __init__(
        self, device: CresControl, path: str, config: EntityDefinition
    ) -> None:
        """Create new CresControl Select Entity."""
        super().__init__(device, path, config)

        # self._attr_state_class = "measurement"
        # self._attr_device_class = path2sensor_device_class(path)
        # self._attr_entity_registry_enabled_default = not config["hidden"]
        # self._attr_entity_registry_enabled_default = path2default_enabled(path)
        # self._attr_native_unit_of_measurement = path2unit(path)
        # self._attr_icon = path2icon(path)
        self._attr_options = path2select_options(path)

    def update_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            self._attr_current_option = str(value)
        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        self.send(f"={option}")

    def update_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        if path.startswith(self.path):
            if path == f"{self.path}":
                self.update_main_value(value)
                return True
        return False
