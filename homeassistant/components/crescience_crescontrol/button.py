"""Crescontrol button entities.

Can be:
- system:reboot()
"""
import logging

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescience.crescontrol import CresControl
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity

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
        if config["type"] == Platform.BUTTON:
            sensor = CresControlButton(hass, device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlButton(CresControlEntity, ButtonEntity):
    """CresControl Button Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device: CresControl,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Button Entity."""
        super().__init__(hass, device, path, config)
        if path == "system:reboot()":
            self._attr_device_class = ButtonDeviceClass.RESTART

    async def async_press(self) -> None:
        """Button press callback."""
        await self._device.send(self.path)
