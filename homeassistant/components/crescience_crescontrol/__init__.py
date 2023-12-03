"""Crescience CresControl local-connection integration."""
# Update device info version
# extra device-Sachen: system:cpu-id, version
# register services like send_message or system:update
# Wie asynchrone Entities?
# Bei Verbindungsabbruch, erneut versuchen
# register intents for Speech
# translations
# connection_status buggy
# update entity

from __future__ import annotations

from collections.abc import Iterable
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, callback
from homeassistant.helpers.entity import Entity

# from homeassistant.helpers.typing import ConfigType
# from homeassistant.helpers.discovery import async_load_platform
from .const import DOMAIN
from .crescience.crescontrol import CresControl

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.FAN,
    Platform.TIME,
    Platform.SELECT,
    Platform.TEXT,
    Platform.BINARY_SENSOR,
    Platform.DATE,
]


def UNDEFINED_async_add_entities(
    new_entities: Iterable[Entity], update_before_add: bool = False
):
    """Add entities to hass dynamically."""
    _LOGGER.error("Cannot add entities dynamically", extra={"list": new_entities})


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry) -> bool:
    """Crescontrol-Entry represents a connection to one CresControl device."""
    # Data that you want to share with your platforms
    hass.data.setdefault(DOMAIN, {"devices": {}})
    uid = config.data.get("uid")
    tag = config.data.get("uid", None)
    host = config.data.get("host")
    assert isinstance(uid, str)
    assert isinstance(host, str)
    device = CresControl(hass, host, uid, tag, UNDEFINED_async_add_entities)
    # device.start(host, 81, False)
    hass.data[DOMAIN]["devices"][uid] = device

    # for platform in PLATFORMS:
    #     hass.async_create_task(
    #         hass.config_entries.async_forward_entry_setup(config, platform)
    #     )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(config, PLATFORMS)
    )

    @callback
    def set_state_service(call: ServiceCall) -> ServiceResponse:
        """Service to send a message."""
        device.send(call.data.get("message", ""))
        return {"status": "ok"}

    # # Register our service with Home Assistant.
    hass.services.async_register(DOMAIN, "send_message", set_state_service)

    device.start(host, 81, False)

    return True
