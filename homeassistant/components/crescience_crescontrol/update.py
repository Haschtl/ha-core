"""Crescontrol update entity.

Used to update the CresControl firmware.
"""
import logging
from typing import Any

from crescience_websocket_py import get_latest_version

from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
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
        if config["type"] == Platform.UPDATE:
            sensor = CresControlUpdate(hass, device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlUpdate(CresControlEntity, UpdateEntity):
    """CresControl Update Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Update Entity."""
        super().__init__(hass, device, path, config)
        self._attr_device_class = UpdateDeviceClass.FIRMWARE
        self._attr_auto_update = False
        self._attr_installed_version = None
        self._attr_latest_version = None
        self._attr_release_url = "https://update.cre.science/crescontrol"
        self._attr_title = "CresControl Firmware"
        self._attr_supported_features = (
            UpdateEntityFeature.INSTALL
            | UpdateEntityFeature.SPECIFIC_VERSION
            | UpdateEntityFeature.PROGRESS
        )
        self._attr_in_progress = False
        self._attr_available = True
        self._attr_entity_registry_enabled_default = True
        self._attr_entity_registry_visible_default = True

    def update_custom(self) -> bool:
        """Update entity cannot update."""
        self._attr_in_progress = False
        if self.path == "firmware:version":
            self.send("firmware:version;firmware:update-server")
        return True

    async def async_update(self) -> None:
        """Update CresControl firmware."""
        self._attr_in_progress = True
        await self.async_send(self.path)

    async def async_install(
        self, version: str | None, backup: bool, **kwargs: Any
    ) -> None:
        """Install an update."""
        self._attr_in_progress = True
        await self.async_send(f"firmware:target-version={version or 'latest'}")
        await self.async_send("firmware:perform-update")

    def fetch_target_version(self):
        """Fetch latest available version from Crescience Update server."""
        if self._attr_release_url is not None:
            latest_version = get_latest_version(self._attr_release_url)
            _LOGGER.info(
                "Checked latest firmware version: %s",
                latest_version["real_version"],
            )
            self._attr_latest_version = latest_version["real_version"]
            self._attr_release_summary = latest_version["summary"]
            self.schedule_update_ha_state()

    @callback
    async def set_custom(self, path: str, value: Any) -> bool:
        """Set installed version."""
        if self.path == "firmware:version":
            if path == self.path:
                self._attr_installed_version = str(value)
                return True
            if path == "firmware:update-server" and isinstance(value, str):
                url = value
                if url.startswith("http"):
                    self._attr_release_url = url
                else:
                    self._attr_release_url = "https://" + url
                # getter = lambda: get_latest_version(url)
                # latest_version = await self.hass.async_add_executor_job(getter)
                # # latest_version = get_latest_version(url)
                # _LOGGER.info(
                #     "Checked latest firmware version: %s",
                #     latest_version["real_version"],
                # )
                # self._attr_latest_version = latest_version["real_version"]
                # self._attr_release_summary = latest_version["summary"]
                # self.schedule_update_ha_state()
                self.hass.async_add_job(self.fetch_target_version)
                return False
        return False
