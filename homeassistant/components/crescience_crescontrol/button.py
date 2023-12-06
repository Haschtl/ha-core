"""Crescontrol button entities.

Can be:
- system:reboot
"""
import logging

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
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
        device,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Button Entity."""
        super().__init__(hass, device, path, config)
        if path == "system:reboot":
            self._attr_device_class = ButtonDeviceClass.RESTART
            self._attr_available = True
            self._attr_entity_registry_enabled_default = True
            self._attr_entity_registry_visible_default = True

    # @property
    # def available(self):
    #     """Buttons are always available, if online."""
    #     return True

    def update(self) -> None:
        """Button entity cannot update."""

    def update_custom(self) -> bool:
        """Button entity cannot be updated."""
        return True

    async def async_press(self) -> None:
        """Button press callback."""
        if self._config["variant"] == "simple":
            await self.async_send(self.path + "()")
        else:
            await self.async_press_custom()

    async def async_press_custom(self):
        """Button press callback for custom entities."""
        if self.path.startswith("radio:device:"):
            feature_name = self.path.split(":")[-1]
            await self.async_send(f'radio:device:transmit("{feature_name}")')
        # elif self.path.startswith("radio:device:off:"):
        #     feature_name = self.path.split(":")[-1]
        #     await self.async_send(f'radio:device:off("{feature_name}")')
        elif self.path.startswith("script:start:"):
            feature_name = self.path.split(":")[-1]
            await self.async_send(f'script:start("{feature_name}")')
        elif self.path.startswith("script:stop:"):
            feature_name = self.path.split(":")[-1]
            await self.async_send(f'script:stop("{feature_name}")')
