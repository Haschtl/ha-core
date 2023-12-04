"""Crescontrol switch entities.

Can be:
- switch-12v
- switch-24v-a
- switch-24v-b
"""
import logging
from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescience.crescontrol import CresControl
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity, UpdateError

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static Switch entities for entry."""
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    sensors = []
    for entity_key, config in STATIC_CRESCONTROL_FEATURES["entities"].items():
        if config["type"] == Platform.SWITCH:
            # and entity_key in extra_sensors:
            sensor = CresControlSwitch(hass, device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlSwitch(CresControlEntity, SwitchEntity):
    """CresControl Switch Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device: CresControl,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Switch Entity."""
        super().__init__(hass, device, path, config)
        self._attr_is_on = False
        self._attr_device_class = SwitchDeviceClass.SWITCH
        # self._attr_icon = path2icon(path)
        # self._attr_entity_registry_enabled_default = path2default_enabled(path)

    @property
    def is_on(self) -> bool | None:
        """If the switch is currently on or off."""
        return self._attr_is_on

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self.send("enabled=true")

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self.send("enabled=true")

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self.send("enabled=false")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self.send("enabled=false")

    def update_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            self._attr_is_on = bool(value)
        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    def pull_custom(self) -> bool:
        """Request the entity data from the device, if entity-type is custom."""
        if self.path in ("fan"):
            return True
            # self._device.send(
            #     f"{self.path}:meta;{self.path}:enabled;{self.path}:pwm-enabled;{self.path}:duty-cycle;{self.path}:pwm-frequency"
            # )
        return False

    def update_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        # if path == self.path:
        #     self.update_main_value(value)
        #     return True
        if path.startswith(self.path + ":"):
            if path == f"{self.path}:voltage":
                self.update_main_value(value)
                return True
            if path == f"{self.path}:enabled":
                return True
        return False
