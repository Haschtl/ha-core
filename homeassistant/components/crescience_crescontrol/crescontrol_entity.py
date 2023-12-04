"""Base entity for all crescontrol entities."""
import logging
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .crescience.crescontrol import CresControl, makeEntityId
from .crescontrol_devices import EntityDefinition
from .helper import path2default_enabled, path2icon, path2nice_name, path2unit

_LOGGER = logging.getLogger(__name__)


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
        self._device.register_update(self.update_state)
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
        #     self.pull(hass)
        # hass.loop.create_task(self.pull())

    # @property
    # def device(self):
    #     """CresControl connection object."""
    #     return self._device

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        self.update()

    def send(self, msg: str):
        """Send a message to this entity."""
        # self._device.send(f"{self.path}:{msg}")
        self.hass.add_job(self._device.send(f"{self.path}:{msg}"))
        # self.hass.loop.create_task(self._device.send(f"{self.path}:{msg}"))

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
            self.pull_custom()

    def pull_custom(self) -> bool:
        """Request the entity data from the device, if entity-type is custom."""
        _LOGGER.warning("Custom components cannot pull")
        return False

    @property
    def available(self):
        """Availability of this entity. It depends on the device-availability."""
        return self._device.available

    # @property
    # def icon(self):
    #     return self._config.get("icon")
    def update_main_value(self, value: Any) -> bool:
        """Update-Callback for child classes."""
        _LOGGER.error("No update_main_value function defined for entity %s", self.path)
        return False

    def update_custom(self, path: str, value: Any) -> bool:
        """Update-Callback for child classes."""
        _LOGGER.error("No update function defined for entity %s", self.path)
        return False

    # @callback
    def update_state(self, path: str, value: Any):
        """Update-routine for CresControl entities."""
        # assert self.entity_id is not None
        if path.startswith(self.path):
            try:
                if self._config["variant"] == "simple":
                    handled = True
                    self.update_main_value(value)
                else:
                    handled = self.update_custom(path, value)
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
            return True
        return False


class UpdateError(Exception):
    """Error while updating entity."""
