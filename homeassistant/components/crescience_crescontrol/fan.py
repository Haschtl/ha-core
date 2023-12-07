"""Crescontrol fan entities.

Can be:
- fan
"""
from typing import Any

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, EntityDefinition
from .crescontrol_entity import CresControlEntity, UpdateError
from .helper import parseBool


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
            sensor = CresControlFan(hass, device, entity_key, config)
            sensors.append(sensor)
    async_add_entities(sensors)


class CresControlFan(CresControlEntity, FanEntity):
    """CresControl Fan Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device,
        path: str,
        config: EntityDefinition,
    ) -> None:
        """Create new CresControl Fan Entity."""
        super().__init__(hass, device, path, config)
        self._attr_supported_features = FanEntityFeature.SET_SPEED
        self.last_percentage = 0

    def set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        self.send(f"duty-cycle={percentage}", True)

    def turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the fan."""
        self.send("enabled=true", True)
        if percentage is not None:
            self.set_percentage(percentage)

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the fan off."""
        self.send("enabled=false", True)

    # async def async_turn_on(self, speed: Optional[str] = None, percentage: Optional[int] = None, preset_mode: Optional[str] = None, **kwargs: Any) -> None:
    #     """Turn on the fan."""

    # async def async_set_percentage(self, percentage: int) -> None:
    #     """Set the speed percentage of the fan."""
    #     self.async_send(f"duty-cycle={percentage}", True)

    def set_main_value(self, value: Any) -> bool:
        """Update the main value of this entity."""
        try:
            if isinstance(value, str):
                enabled = parseBool(value)
            else:
                enabled = bool(value)
            if enabled:
                self._attr_percentage = self.last_percentage
            else:
                self._attr_percentage = 0
        except Exception as exc:
            raise UpdateError(exc) from exc
        return True

    def update_custom(self) -> bool:
        """Request the entity data from the device, if entity-type is custom."""
        if self.path in ("fan"):
            self.send(f"{self.path}:duty-cycle;{self.path}:enabled;")
            return True
        return False

    async def set_custom(self, path: str, value: Any) -> bool:
        """Update entity with type=='custom'."""
        # if path == self.path:
        #     self.set_main_value(value)
        #     return True
        if path.startswith(self.path + ":"):
            if path == f"{self.path}:enabled":
                self.set_main_value(value)
                return True
            if path == f"{self.path}:duty-cycle":
                try:
                    self._attr_percentage = int(float(value))
                    self.last_percentage = int(float(value))
                except Exception as exc:
                    raise UpdateError(exc) from exc
                return True
            # elif path == f"{self.path}:rpm":
            #     self._attr_percentage = int(value)
            #     return True
        return False
