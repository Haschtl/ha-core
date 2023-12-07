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
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity, UpdateError
from .helper import parseBool

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
        device,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Switch Entity."""
        super().__init__(hass, device, path, config)
        self._attr_is_on = False
        self._attr_device_class = SwitchDeviceClass.SWITCH
        # self._attr_icon = path2icon(path)
        # self._attr_entity_registry_enabled_default = path2default_enabled(path)

    # @property
    # def is_on(self) -> bool | None:
    #     """If the switch is currently on or off."""
    #     return self._attr_is_on

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        if self._config["variant"] == "simple":
            self.send(self.path + "=true")
        else:
            self.turn_on_custom()

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        if self._config["variant"] == "simple":
            self.send(self.path + "=false")
        else:
            self.turn_off_custom()

    def set_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            if isinstance(value, str):
                self._attr_is_on = parseBool(value)
            else:
                self._attr_is_on = bool(value)
        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    def update_custom(self) -> bool:
        """Request the entity data from the device, if entity-type is custom."""
        if self.path.startswith("switch-"):
            self.send(self.path + ":enabled")
            return True
        if self.path.startswith("schedule:"):
            return True
        if self.path.startswith("stabilization:bang-bang:"):
            return True
        if self.path.startswith("stabilization:pid:"):
            return True
        return False

    async def set_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        if self.path.startswith("switch-"):
            if path == f"{self.path}:enabled":
                self.set_main_value(value)
                return True
        if self.path.startswith("schedule:"):
            return False
        if self.path.startswith("stabilization:bang-bang:"):
            return False
        if self.path.startswith("stabilization:pid:"):
            return False
        return False

    def turn_off_custom(self) -> bool:
        """Turn device off, if entity-type is custom."""
        return self.toggle_custom(False)

    def turn_on_custom(self) -> bool:
        """Turn device on, if entity-type is custom."""
        return self.toggle_custom(True)

    def toggle_custom(self, value: bool):
        """Toggle function for custom switches."""
        set_value = "true" if value else "false"
        if self.path.startswith("switch-"):
            self.send(f"enabled={set_value}")
            return True
        if (
            self.path.startswith("schedule:")
            or self.path.startswith("stabilization:bang-bang:")
            or self.path.startswith("stabilization:pid:")
        ):
            feature_name = self.path.split(":")[-1]
            feature_path = ":".join(self.path.split(":")[0:-1])
            self.send(f'{feature_path}:set-enabled("{feature_name}",{set_value})')

            return True
        return False
