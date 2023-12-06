"""CresControl object for local connection with home-assistant."""
from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any

import aiohttp

import homeassistant.components.crescience_crescontrol.binary_sensor
import homeassistant.components.crescience_crescontrol.button
import homeassistant.components.crescience_crescontrol.crescontrol_entity
import homeassistant.components.crescience_crescontrol.date
import homeassistant.components.crescience_crescontrol.fan
import homeassistant.components.crescience_crescontrol.number
import homeassistant.components.crescience_crescontrol.select
import homeassistant.components.crescience_crescontrol.sensor
import homeassistant.components.crescience_crescontrol.switch
import homeassistant.components.crescience_crescontrol.text
import homeassistant.components.crescience_crescontrol.time
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import EntityPlatform

from ..crescontrol_devices import EntityDefinition
from .client import (
    ConnectionErrorReason,
    ConnectionMessageType,
    ConnectionState,
    WebsocketClient,
)
from .helper import represents_number
from .message import Message

_LOGGER = logging.getLogger(__name__)


# class CresControlEntity(Entity):
#     """Dummy-entity to avoid circular import."""

#     def set_main_value(self, value: Any):
#         """Update main value."""


class CresControl(WebsocketClient):
    """CresControl object for local connection with home-assistant."""

    def __init__(
        self,
        hass: HomeAssistant,
        domain: str,
        config: ConfigEntry,
        host: str,
        uid: str,
        tag: str | None,
        callback: Callable[
            [ConnectionMessageType, str | None, ConnectionErrorReason | None], None
        ]
        | None,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initialize CresControl object inside home-assistant."""
        super().__init__(host, 81, None, False, callback, session)
        self.uid = uid
        self.tag = tag
        self.messageQueue: list[str] = []
        self.hass = hass
        self._config = config
        self.connected_entity: homeassistant.components.crescience_crescontrol.binary_sensor.CresControlBinarySensor | None = None
        self.connection_status_entity: homeassistant.components.crescience_crescontrol.sensor.CresControlSensor | None = None
        self.dynamicEntities: dict[
            str,
            homeassistant.components.crescience_crescontrol.crescontrol_entity.CresControlEntity,
        ] = {}
        self.entity_update_callbacks: list[Callable[[str, Any], bool]] = []
        self.status_entity_id = domain + ".status_" + uid.replace("-", "_")

    @property
    def available(self):
        """Device is available."""
        return self.state == ConnectionState.CONNECTED

    # def start(self,host:str):
    #     self.start(host, 81, False)

    # @callback
    def _received_registered_entity(self, path: str, value: Any) -> bool:
        handled = False
        if len(self.entity_update_callbacks) == 0:
            _LOGGER.error("No entities registered for CresControl")
            return True
        for cb in self.entity_update_callbacks:
            # cb(path, value)
            handled = cb(path, value)
            if handled:
                break
        return handled

    # @callback
    def _received_dynamic_entity(self, path: str, value: Any) -> bool:
        # entity_id = makeEntityId(self.uid, path)
        if path in self.dynamicEntities:
            if represents_number(value):
                self.dynamicEntities[path].set_state(path, float(value))
            else:
                self.dynamicEntities[path].set_state(path, str(value))
            # self.dynamicEntities[path].set_main_value(value)
            self.dynamicEntities[path].schedule_update_ha_state()
        else:
            self.createDynamicSensorEntity(path, value)
        return True

    # @callback
    async def received(self, msg: Message) -> None:
        """CresNet message received callback."""
        if isinstance(msg.returns, list):
            for idx, command in enumerate(msg.commands):
                if command.typ == "parameterGet":
                    path = ":".join(command.path)
                    # _LOGGER.warning("Message received %s::%s", path, msg.returns[idx])

                    # handled = False
                    # for cb in self.entity_update_callbacks:
                    #     handled = cb(path, msg.returns[idx])
                    #     if handled:
                    #         break
                    # try:
                    handled = self._received_registered_entity(path, msg.returns[idx])
                    # except Exception:
                    #     _LOGGER.exception("Handling command failed")
                    #     handled = True
                    if not handled:
                        # !!! dynamic disabled
                        # pass
                        handled = self._received_dynamic_entity(path, msg.returns[idx])

    # @callback
    async def on_close(self, *args):
        """Websocket connection closed callback."""
        _LOGGER.warning("Connection with %s closed", self.uid)
        self.set_status("closed")

    # @callback
    async def on_open(self):
        """Websocket connection opened callback."""
        _LOGGER.info("Connection with %s opened", self.uid)
        await self.send(
            "subscription:subscribe();out-a:voltage;out-b:voltage;out-c:voltage;out-d:voltage;out-e:voltage;out-f:voltage;fan:rpm;switch-12v:enabled;switch-24v-a:enabled;switch-24v-b:enabled;fan:duty-cycle"
        )
        if len(self.messageQueue) > 0:
            for message in self.messageQueue:
                await self.send(message)
            self.messageQueue = []
        self.set_status("connected")

    # @callback
    async def on_error(self, error, *args):
        """Websocket connection error callback."""
        _LOGGER.warning("Connection with %s error", self.uid)
        self.set_status("error")

    def update_status(self):
        """Update the status entities."""
        state = self.state
        if self._error_reason is not None:
            self.set_status("error")
        elif state == ConnectionState.CONNECTED:
            self.set_status("connected")
        elif state == ConnectionState.DISCONNECTED:
            self.set_status("closed")

    def set_status(self, value: str):
        """Update the connection status entities."""  #
        if self.connection_status_entity is not None:
            self.connection_status_entity._attr_native_value = str(value)  # pylint: disable=protected-access
            # self.connection_status_entity.set_main_value(value)
            self.connection_status_entity.schedule_update_ha_state()
        else:
            _LOGGER.warning(
                "Cannot set device status to '%s', no connection-status-entity registered. This is expected, if the update-entity is disabled",
                value,
            )
        if self.connected_entity is not None:
            self.connected_entity._attr_is_on = value in ("connected")  # pylint: disable=protected-access
            # self.connected_entity.set_main_value(value in ("connected"))
            self.connected_entity.schedule_update_ha_state()
        else:
            _LOGGER.warning(
                "Cannot set device status to '%s', no connected-entity registered. This is expected, if the update-state-entity is disabled",
                value,
            )
        # self.hass.states.async_set(self.status_entity_id, "error")

    def createDynamicSensorEntity(self, path: str, initValue: Any):
        """Create a dynamic sensor-entity. Used for CresControl extensions."""
        sensor = self.add_entity(
            path,
            {
                "type": Platform.SENSOR,
                "variant": "simple",
                "category": None,
                "sensor_class": None,
            },
        )
        sensor.set_main_value(initValue)

    def add_entity(
        self,
        path: str,
        config: EntityDefinition,
    ):
        """Add an entity to this device."""
        _LOGGER.info("Creating new dynamic sensor for %s", path)
        # from ..crescontrol_entity import (  # pylint: disable=import-outside-toplevel
        #     CresControlEntity,
        # )

        entity: homeassistant.components.crescience_crescontrol.crescontrol_entity.CresControlEntity
        if config["type"] == Platform.BUTTON:
            entity = homeassistant.components.crescience_crescontrol.button.CresControlButton(
                self.hass, self, path, config
            )
        elif config["type"] == Platform.BINARY_SENSOR:
            entity = homeassistant.components.crescience_crescontrol.binary_sensor.CresControlBinarySensor(
                self.hass, self, path, config
            )
        elif config["type"] == Platform.DATE:
            entity = (
                homeassistant.components.crescience_crescontrol.date.CresControlDate(
                    self.hass, self, path, config
                )
            )
        elif config["type"] == Platform.FAN:
            entity = homeassistant.components.crescience_crescontrol.fan.CresControlFan(
                self.hass, self, path, config
            )
        elif config["type"] == Platform.NUMBER:
            entity = homeassistant.components.crescience_crescontrol.number.CresControlNumber(
                self.hass, self, path, config
            )
        elif config["type"] == Platform.SELECT:
            entity = homeassistant.components.crescience_crescontrol.select.CresControlSelect(
                self.hass, self, path, config
            )
        elif config["type"] == Platform.SENSOR:
            entity = homeassistant.components.crescience_crescontrol.sensor.CresControlSensor(
                self.hass, self, path, config
            )
        elif config["type"] == Platform.SWITCH:
            entity = homeassistant.components.crescience_crescontrol.switch.CresControlSwitch(
                self.hass, self, path, config
            )
        elif config["type"] == Platform.TEXT:
            entity = (
                homeassistant.components.crescience_crescontrol.text.CresControlText(
                    self.hass, self, path, config
                )
            )
        elif config["type"] == Platform.TIME:
            entity = (
                homeassistant.components.crescience_crescontrol.time.CresControlTime(
                    self.hass, self, path, config
                )
            )
        else:
            raise NotImplementedError(
                f"Dynamic entities of type {config['type']} are not implemented."
            )
        entity._attr_entity_registry_enabled_default = True  # pylint: disable=protected-access
        self.hass.async_add_job(self._platform.async_add_entities([entity]))
        self.dynamicEntities[path] = entity
        # sensor.schedule_update_ha_state()
        return entity

    @property
    def _platform(self):
        entity_component = self.hass.data["sensor"]  # EntityComponent for sensor
        entity_platform: EntityPlatform = entity_component._platforms[  # pylint: disable=protected-access
            self._config.entry_id
        ]
        return entity_platform

    # @callback
    def register_update(self, cb: Callable[[str, Any], bool]):
        """Register a new entity, which needs updates."""
        self.entity_update_callbacks.append(cb)

    def set_online_status_entity(
        self,
        entity: homeassistant.components.crescience_crescontrol.sensor.CresControlSensor,
    ):
        """Set the connection-status entity for this CresControl."""
        self.connection_status_entity = entity
        # self.connection_status_entity.hass = self.hass

    def set_connected_entity(
        self,
        entity: homeassistant.components.crescience_crescontrol.binary_sensor.CresControlBinarySensor,
    ):
        """Set the connected entity for this CresControl."""
        self.connected_entity = entity
        # self.connected_entity.hass = self.hass

    # def send(self, msg: str):
    #     """Send a message to the host."""

    #     if self.ws is None or not self.available:
    #         self.messageQueue.append(msg)
    #         return
    #     # if self.crypto is not None:
    #     #     msg = self.crypto.encrypt(msg)

    #     self.ws.send(msg)
