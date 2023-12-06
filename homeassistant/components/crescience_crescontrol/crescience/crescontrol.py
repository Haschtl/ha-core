"""CresControl object for local connection with home-assistant."""
from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import EntityPlatform

from ..binary_sensor import CresControlBinarySensor
from ..button import CresControlButton
from ..crescontrol_devices import EntityDefinition, path2entity_definition
from ..crescontrol_entity import CresControlEntity
from ..date import CresControlDate
from ..fan import CresControlFan
from ..number import CresControlNumber
from ..select import CresControlSelect
from ..sensor import CresControlSensor
from ..switch import CresControlSwitch
from ..text import CresControlText
from ..time import CresControlTime
from .client import (
    ConnectionErrorReason,
    ConnectionMessageType,
    ConnectionState,
    WebsocketClient,
)
from .helper import represents_number
from .message import Command, Message

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
        super().__init__(
            host, 81, None, False, callback, session, max_failed_attempts=-1
        )
        self.uid = uid
        self.tag = tag
        self.messageQueue: list[str] = []
        self.hass = hass
        self._config = config
        self.connected_entity: CresControlBinarySensor | None = None
        self.connection_status_entity: CresControlSensor | None = None
        self.dynamicEntities: dict[
            str,
            CresControlEntity,
        ] = {}
        self.entity_update_callbacks: list[
            Callable[[str | None, Any, ConnectionMessageType | None], bool]
        ] = []
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
            handled = cb(path, value, None)
            if handled:
                break
        return handled

    # @callback
    def _received_dynamic_entity(self, command: Command, value: Any) -> bool:
        # entity_id = makeEntityId(self.uid, path)
        path = find_feature_path(command, value)
        if path in self.dynamicEntities:
            if represents_number(value):
                self.dynamicEntities[path].set_state(path, float(value), None)
            else:
                self.dynamicEntities[path].set_state(path, str(value), None)
            # self.dynamicEntities[path].set_main_value(value)
            self.dynamicEntities[path].schedule_update_ha_state()
        elif path.endswith("get-all"):
            if isinstance(value, list):
                if len(value) > 0:
                    for feature in value:
                        if path == "script:get-all":
                            self.add_script(feature)
                        elif path == "schedule:get-all":
                            self.add_schedule(feature)
                        elif path == "radio:remote:get-all":
                            self.add_radio_remote(feature)
                        elif path == "radio:device:get-all":
                            self.add_radio_device(feature)
                        elif path == "stabilization:bang-bang:get-all":
                            self.add_stabilization_bang_bang(feature)
                        elif path == "stabilization:pid:get-all":
                            self.add_stabilization_pid(feature)
                        else:
                            _LOGGER.warning(
                                "Cannot handle this get-all() message: %s", path
                            )
            else:
                _LOGGER.error(
                    "Cannot handle this get-all() message. Return type is wrong: %s",
                    path,
                )

        else:
            self.add_dynamic_entity(path, value)
        return True

    # @callback
    async def received(self, msg: Message) -> None:
        """CresNet message received callback."""
        if isinstance(msg.returns, list):
            for idx, command in enumerate(msg.commands):
                if command.typ in ("parameterGet", "functionCall"):
                    path = ":".join(command.path)
                    if path not in ("subscription:subscribe"):
                        handled = self._received_registered_entity(
                            path, msg.returns[idx]
                        )
                        if not handled:
                            handled = self._received_dynamic_entity(
                                command, msg.returns[idx]
                            )

    # @callback
    async def on_close(self, *args):
        """Websocket connection closed callback."""
        _LOGGER.warning("Connection with %s closed", self.uid)
        self.set_status("closed")
        for cb in self.entity_update_callbacks:
            cb(None, None, ConnectionMessageType.CLOSED)

    # @callback
    async def on_open(self):
        """Websocket connection opened callback."""
        _LOGGER.info("Connection with %s opened", self.uid)
        # await self.send(
        #     "subscription:subscribe();out-a:voltage;out-b:voltage;out-c:voltage;out-d:voltage;out-e:voltage;out-f:voltage;fan:rpm;switch-12v:enabled;switch-24v-a:enabled;switch-24v-b:enabled;fan:duty-cycle"
        # )
        await self.send(
            "subscription:subscribe();script:get-all();schedule:get-all();radio:remote:get-all();radio:device:get-all();stabilization:bang-bang:get-all();stabilization:pid:get-all()"
        )
        if len(self.messageQueue) > 0:
            for message in self.messageQueue:
                await self.send(message)
            self.messageQueue = []
        self.set_status("connected")
        for cb in self.entity_update_callbacks:
            cb(None, None, ConnectionMessageType.OPEN)

    # @callback
    async def on_error(self, error, *args):
        """Websocket connection error callback."""
        _LOGGER.warning("Connection with %s error", self.uid)
        self.set_status("error")
        for cb in self.entity_update_callbacks:
            cb(None, None, ConnectionMessageType.ERROR)

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
                "Cannot set device status to '%s', no connection-status-entity registered. This is expected, if the connection-status-entity is disabled",
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

    def add_dynamic_entity(self, path: str, initValue: Any):
        """Create a dynamic sensor-entity. Used for CresControl extensions."""
        sensor = self.add_entity(path, path2entity_definition(path))
        if initValue is not None:
            sensor.set_main_value(initValue)

    def add_entity(self, path: str, config: EntityDefinition, enabled_default=True):
        """Add an entity to this device."""
        _LOGGER.info("Creating new dynamic %s for %s", config["type"], path)
        # from ..crescontrol_entity import (  # pylint: disable=import-outside-toplevel
        #     CresControlEntity,
        # )

        entity: CresControlEntity
        if config["type"] == Platform.BUTTON:
            entity = CresControlButton(self.hass, self, path, config)
        elif config["type"] == Platform.BINARY_SENSOR:
            entity = CresControlBinarySensor(self.hass, self, path, config)
        elif config["type"] == Platform.DATE:
            entity = CresControlDate(self.hass, self, path, config)
        elif config["type"] == Platform.FAN:
            entity = CresControlFan(self.hass, self, path, config)
        elif config["type"] == Platform.NUMBER:
            entity = CresControlNumber(self.hass, self, path, config)
        elif config["type"] == Platform.SELECT:
            entity = CresControlSelect(self.hass, self, path, config)
        elif config["type"] == Platform.SENSOR:
            entity = CresControlSensor(self.hass, self, path, config)
        elif config["type"] == Platform.SWITCH:
            entity = CresControlSwitch(self.hass, self, path, config)
        elif config["type"] == Platform.TEXT:
            entity = CresControlText(self.hass, self, path, config)
        elif config["type"] == Platform.TIME:
            entity = CresControlTime(self.hass, self, path, config)
        else:
            raise NotImplementedError(
                f"Dynamic entities of type {config['type']} are not implemented."
            )
        entity._attr_entity_registry_enabled_default = enabled_default  # pylint: disable=protected-access
        self.hass.async_add_job(
            self.get_platform(config["type"]).async_add_entities([entity])
        )
        self.dynamicEntities[path] = entity
        # sensor.schedule_update_ha_state()
        return entity

    def get_platform(self, platform: Platform = Platform.SENSOR):
        """Get platform for given platform."""
        entity_component = self.hass.data[platform]  # EntityComponent for sensor
        entity_platform: EntityPlatform = entity_component._platforms[  # pylint: disable=protected-access
            self._config.entry_id
        ]
        return entity_platform

    # @callback
    def register_update(
        self, cb: Callable[[str | None, Any, ConnectionMessageType | None], bool]
    ):
        """Register a new entity, which needs updates."""
        self.entity_update_callbacks.append(cb)

    def set_online_status_entity(
        self,
        entity: CresControlSensor,
    ):
        """Set the connection-status entity for this CresControl."""
        self.connection_status_entity = entity
        # self.connection_status_entity.hass = self.hass

    def set_connected_entity(
        self,
        entity: CresControlBinarySensor,
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

    def add_script(self, name: str):
        """Add dynamic entities for scripts."""
        _LOGGER.info("Adding entities for script: %s", name)
        start_path = f"script:start:{name}"
        stop_path = f"script:stop:{name}"
        self.add_entity(
            start_path,
            {
                "type": Platform.BUTTON,
                "category": EntityCategory.CONFIG,
                "sensor_class": None,
                "variant": "custom",
            },
        )
        self.add_entity(
            stop_path,
            {
                "type": Platform.BUTTON,
                "category": EntityCategory.CONFIG,
                "sensor_class": None,
                "variant": "custom",
            },
        )

    def add_schedule(self, name: str):
        """Add dynamic entity for schedule."""
        _LOGGER.info("Adding entity for schedule: %s", name)
        self.add_entity(
            f"schedule:{name}",
            {
                "type": Platform.SWITCH,
                "category": EntityCategory.CONFIG,
                "sensor_class": None,
                "variant": "custom",
            },
        )

    def add_radio_remote(self, name: str):
        """Add dynamic entity for radio:remote."""
        _LOGGER.warning("Adding entity for radio:remote: %s is not supported", name)
        # self.add_entity(
        #     f"schedule:{name}",
        #     {
        #         "type": Platform.SWITCH,
        #         "category": EntityCategory.CONFIG,
        #         "sensor_class": None,
        #         "variant": "custom",
        #     },
        # )

    def add_radio_device(self, name: str):
        """Add dynamic entity for radio:device."""
        _LOGGER.info("Adding entity for radio:device: %s", name)
        # start_path = f"radio:device:on:{name}"
        start_path = f"radio:device:{name}"
        # stop_path = f"radio:device:off:{name}"
        self.add_entity(
            start_path,
            {
                "type": Platform.BUTTON,
                "category": EntityCategory.CONFIG,
                "sensor_class": None,
                "variant": "custom",
            },
        )
        # self.add_entity(
        #     stop_path,
        #     {
        #         "type": Platform.BUTTON,
        #         "category": EntityCategory.CONFIG,
        #         "sensor_class": None,
        #         "variant": "custom",
        #     },
        # )

    def add_stabilization_bang_bang(self, name: str):
        """Add dynamic entity for stabilization:bang-bang."""
        _LOGGER.info("Adding entity for stabilization:bang-bang: %s", name)
        self.add_entity(
            f"stabilization:bang-bang:{name}",
            {
                "type": Platform.SWITCH,
                "category": EntityCategory.CONFIG,
                "sensor_class": None,
                "variant": "custom",
            },
        )

    def add_stabilization_pid(self, name: str):
        """Add dynamic entity for stabilization:pid."""
        _LOGGER.info("Adding entity for stabilization:pid: %s", name)
        self.add_entity(
            f"stabilization:pid:{name}",
            {
                "type": Platform.SWITCH,
                "category": EntityCategory.CONFIG,
                "sensor_class": None,
                "variant": "custom",
            },
        )


def find_feature_path(command: Command, value: Any):
    """Check for CresControl feature paths registered as dynamic entity."""
    path = ":".join(command.path)
    if (
        command.typ == "functionCall"
        and command.func_parameters is not None
        and len(command.func_parameters) > 0
    ):
        if path.startswith("stabilization:bang-bang:"):
            return f"stabilization:bang-bang:{str(command.func_parameters[0])}"
        if path.startswith("stabilization:pid:"):
            return f"stabilization:pid:{str(command.func_parameters[0])}"
        if path.startswith("schedule:"):
            return f"schedule:{str(command.func_parameters[0])}"
        if path.startswith("radio:device:"):
            return f"radio:device:{str(command.func_parameters[0])}"
        if path.startswith("radio:remote:"):
            return f"radio:remote:{str(command.func_parameters[0])}"
        if path.startswith("script:"):
            return f"script:{str(command.func_parameters[0])}"
    return path
