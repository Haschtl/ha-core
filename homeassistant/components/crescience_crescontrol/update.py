"""Crescontrol update entity.

Used to update the CresControl firmware.
"""
import logging
from typing import Any

from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityFeature,
)
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
        if config["type"] == Platform.UPDATE:
            sensor = CresControlUpdate(hass, device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlUpdate(CresControlEntity, UpdateEntity):
    """CresControl Update Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device: CresControl,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Update Entity."""
        super().__init__(hass, device, path, config)
        self._attr_device_class = UpdateDeviceClass.FIRMWARE
        self._attr_auto_update = False
        self._attr_installed_version = "0.0.0"
        self._attr_latest_version = "0.0.0"
        self._attr_title = "CresControl Firmware"
        self._attr_supported_features = (
            UpdateEntityFeature.INSTALL | UpdateEntityFeature.SPECIFIC_VERSION
        )

    async def async_update(self) -> None:
        """Update CresControl firmware."""
        await self._device.send(self.path)

    async def async_install(
        self, version: str | None, backup: bool, **kwargs: Any
    ) -> None:
        """Install an update."""
        await self._device.send(f"firmware:target-version={version or 'latest'}")
        _LOGGER.error("Install update is not implemented")
        await self._device.send(self.path)
