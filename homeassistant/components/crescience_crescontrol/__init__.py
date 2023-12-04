"""Crescience CresControl local-connection integration."""
# Fixen:
# Connected-state funktioniert nicht
# Wie asynchrone Entities?

# Update device info version
# extra device-Sachen: system:cpu-id, version
# register services like send_message or system:update
# Bei Verbindungsabbruch, erneut versuchen
# register intents for Speech
# translations
# connection_status buggy
# update entity

from __future__ import annotations

from collections.abc import Iterable
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity

# from homeassistant.helpers.typing import ConfigType
# from homeassistant.helpers.discovery import async_load_platform
# from .crescience.client import ConnectionErrorReason, ConnectionMessageType
from .const import DOMAIN
from .crescience.crescontrol import CresControl

_LOGGER = logging.getLogger(__name__)
PLATFORMS = frozenset(
    [
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
)


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

    # @callback
    # def cresnet_websocket_callback(msgtype:ConnectionMessageType, data:str, error:ConnectionErrorReason):
    #     _LOGGER.info(msgtype, data, error)
    #     if msgtype==ConnectionMessageType.TEXT:

    session = async_get_clientsession(hass)
    device = CresControl(
        hass,
        host,
        uid,
        tag,
        UNDEFINED_async_add_entities,
        # cresnet_websocket_callback,
        None,
        session,
    )
    # device.start(host, 81, False)
    hass.data[DOMAIN]["devices"][uid] = device
    # hass.loop.create_task(device.listen())
    # for platform in PLATFORMS:
    #     hass.async_create_task(
    #         hass.config_entries.async_forward_entry_setup(config, platform)
    #     )
    # hass.async_create_task(
    # )
    await hass.config_entries.async_forward_entry_setups(config, PLATFORMS)

    @callback
    def set_state_service(call: ServiceCall) -> ServiceResponse:
        """Service to send a message."""
        hass.loop.create_task(device.send(call.data.get("message", "")))
        return {"status": "ok"}

    def close_websocket_session(_):
        device.close()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, close_websocket_session)

    # # Register our service with Home Assistant.
    hass.services.async_register(DOMAIN, "send_message", set_state_service)
    hass.loop.create_task(device.listen())

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    uid = config_entry.data.get("uid")
    hass.data[DOMAIN]["devices"][uid].close()

    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    hass.data[DOMAIN]["devices"].pop(uid)

    return unload_ok
