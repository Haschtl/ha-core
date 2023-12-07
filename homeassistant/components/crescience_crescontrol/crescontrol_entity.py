"""Base entity for all crescontrol entities."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

if TYPE_CHECKING:
    from .crescience.client import ConnectionMessageType
    from .crescience.crescontrol import CresControl
from .crescontrol_devices import EntityDefinition
from .helper import path2default_enabled, path2icon, path2nice_name, path2unit

_LOGGER = logging.getLogger(__name__)


def makeEntityId(uid: str, path: str):
    """Generate unique Entity-ID for given device-uid and CresControl path."""
    return (
        f"{DOMAIN}.{uid.replace('-', '_')}_p_{path.replace('-', '_').replace(':', '_')}"
    )


class CresControlEntity(Entity):
    """Base entity for all crescontrol entities."""

    _attr_has_entity_name = True
    _attr_entity_registry_visible_default = True
    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        device: CresControl,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Initialize the crescontrol entity."""
        self._device = device
        self._config = config
        self._device.register_update(self.set_state)
        self._attr_entity_registry_enabled_default = path2default_enabled(path)
        self._attr_native_unit_of_measurement = path2unit(path)
        self._attr_entity_category = config["category"]
        self._attr_icon = path2icon(path)
        self.uid: str = device.uid
        self.path = path
        self._attr_name = path2nice_name(path)
        # self._attr_unique_id = f"{DOMAIN}.{self.uid}_{path}"
        self._attr_unique_id = makeEntityId(self.uid, path)
        self._attr_translation_key = self.uid
        # self.hass = hass
        # if self.enabled and self._config["variant"] == "simple":
        # if self.enabled:
        #     self.update(hass)
        # hass.loop.create_task(self.update())

    # @property
    # def device(self):
    #     """CresControl connection object."""
    #     return self._device

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        self.update()
        if self.path == "connection_status":
            self._device.set_online_status_entity(self)  # type: ignore[arg-type]
            self._device.update_status()
        if self.path == "connected":
            self._device.set_connected_entity(self)  # type: ignore[arg-type]
            self._device.update_status()

    def send(self, msg: str, prefix=False):
        """Send a message to this entity."""
        if prefix:
            self.hass.add_job(self._device.send(f"{self.path}:{msg}"))
        else:
            self.hass.add_job(self._device.send(msg))

    async def async_send(self, msg: str, prefix=False):
        """Send a message to this entity."""
        if prefix:
            await self._device.send(f"{self.path}:{msg}")
        else:
            await self._device.send(msg)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.uid)
            },
            name=self.uid,
            # name=self._device.tag,
            manufacturer="Crescience",
            model="CresControl V1",
            # sw_version=self.light.swversion,
            # via_device=(hue.DOMAIN, self.api.bridgeid),
        )

    # @property
    # def unique_id(self):
    #     return self._attr_unique_id

    # @property
    # def should_poll(self):
    #     return False

    # @property
    # def name(self):
    #     return (
    #         f"{self._device_name} {self._config.get('name')}"
    #         if "name" in self._config
    #         else self._device_name
    #     )

    @callback
    def update(self):
        """Request the entity data from the device."""
        # if not self.enabled:
        #     return
        if self._config["variant"] == "simple":
            # if queue:
            #     self._device.message_queue.append(self.path)
            # else:
            # if hass is not None:
            #     hass.add_job(self._device.send(self.path))
            if self.hass is not None:
                self.hass.add_job(self._device.send(self.path))
            else:
                _LOGGER.warning(
                    "Entity %s not initialized. Message is added to queue", self.uid
                )
                self._device.message_queue.append(self.path)
        # self.hass.loop.create_task(self._device.send(self.path))
        else:
            self.update_custom()

    def update_custom(self) -> bool:
        """Request the entity data from the device, if entity-type is custom."""
        _LOGGER.warning("Custom components cannot be updated")
        return False

    @property
    def available(self):
        """Availability of this entity. It depends on the device-availability."""
        return self._device.available

    # @property
    # def icon(self):
    #     return self._config.get("icon")
    def set_main_value(self, value: Any) -> bool:
        """Update-Callback for child classes."""
        _LOGGER.error("No set_main_value function defined for entity %s", self.path)
        return False

    async def set_custom(self, path: str, value: Any) -> bool:
        """Update-Callback for child classes."""
        _LOGGER.error("No custom set function defined for entity %s", self.path)
        return False

    # @callback
    async def set_state(
        self, path: str | None, value: Any, device_status: ConnectionMessageType | None
    ) -> bool:
        """Update-routine for CresControl entities."""
        # assert self.entity_id is not None
        if path is not None and value is not None:
            return await self._set_state(path, value)
        if device_status is not None:
            return self._handle_device_change(device_status)
        return False

    def _handle_device_change(self, device_status: ConnectionMessageType) -> bool:
        if self.enabled:
            try:
                self.schedule_update_ha_state()
            except (RuntimeError, AttributeError):
                _LOGGER.exception(
                    "Entity %s update_state failed device_status = %s",
                    self.entity_id,
                    device_status,
                )
        return True

    async def _set_state(self, path: str, value: Any) -> bool:
        """Update-routine for CresControl entities."""
        # if path.startswith(self.path):
        try:
            handled = False
            if path.startswith(self.path) and self._config["variant"] == "simple":
                handled = True
                self.set_main_value(value)
            elif self._config["variant"] == "custom":
                handled = await self.set_custom(path, value)
        except UpdateError:
            _LOGGER.exception(
                "Error while updating %s:%s: %s::%s",
                self.uid,
                self.path,
                path,
                value,
            )
            handled = True
        # if not handled:
        #     _LOGGER.warning(
        #         "Message was not handled by entity %s: %s:%s",
        #         self.path,
        #         path,
        #         value,
        #     )
        if handled and self.enabled:
            try:
                self.schedule_update_ha_state()
            except (RuntimeError, AttributeError):
                # except Exception:
                _LOGGER.exception(
                    "Entity %s update_state failed path = %s, value = %s",
                    self.entity_id,
                    path,
                    value,
                )
        return handled
        # return False


class UpdateError(Exception):
    """Error while updating entity."""
