"""Crescontrol fan entities.

Can be:
- fan
"""
from typing import Any

from homeassistant.components.fan import FanEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES
from .crescontrol_entity import CresControlEntity, UpdateError


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static Fan entities for entry."""
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    sensors = []
    for entity_key, config in STATIC_CRESCONTROL_FEATURES["entities"].items():
        if config["type"] == Platform.FAN:
            # and entity_key in extra_sensors:
            sensor = CresControlFan(device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlFan(CresControlEntity, FanEntity):
    """CresControl Fan Entity."""

    # def __init__(
    #     self, device: CresControl, path: str, config: EntityDefinition
    # ) -> None:
    #     """Create new CresControl Fan Entity."""
    #     super().__init__(device, path, config)
    #     # self._attr_entity_registry_enabled_default = path2default_enabled(path)

    def set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        self.send(f"duty-cycle={percentage}")

    def turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the fan."""
        self.send("enabled=true")
        if percentage is not None:
            self.set_percentage(percentage)

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the fan off."""
        self.send("enabled=false")

    # async def async_turn_on(self, speed: Optional[str] = None, percentage: Optional[int] = None, preset_mode: Optional[str] = None, **kwargs: Any) -> None:
    #     """Turn on the fan."""

    # async def async_set_percentage(self, percentage: int) -> None:
    #     """Set the speed percentage of the fan."""
    #     self.send(f"duty-cycle={percentage}")

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
            # self.device.send(
            #     f"{self.path}:meta;{self.path}:enabled;{self.path}:duty-cycle;{self.path}:duty-cycle-min;{self.path}:rpm;{self.path}:rpm-prescaler;{self.path}:vcc-pwm;{self.path}:vcc-pwm-frequency"
            # )
        return False

    def update_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        # if path == self.path:
        #     self.update_main_value(value)
        #     return True
        if path.startswith(self.path + ":"):
            if path == f"{self.path}:enabled":
                self.update_main_value(value)
                return True
            if path == f"{self.path}:duty-cycle":
                try:
                    self._attr_percentage = int(float(value))
                except Exception as exc:
                    raise UpdateError(exc) from exc
                return True
            # elif path == f"{self.path}:rpm":
            #     self._attr_percentage = int(value)
            #     return True
        return False
