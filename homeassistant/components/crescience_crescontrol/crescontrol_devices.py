"""Definition of CresControl hardware/software variants."""
import logging
from typing import Literal, TypedDict

from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import EntityCategory, Platform

_LOGGER = logging.getLogger(__name__)


class EntityDefinition(TypedDict):
    """Definition of a CresControl entity."""

    type: Platform
    variant: Literal["simple", "custom"]
    category: EntityCategory | None
    sensor_class: SensorStateClass | None


class FeatureObject(TypedDict):
    """Definition of CresControl entities."""

    entities: dict[str, EntityDefinition]


STATIC_CRESCONTROL_FEATURES: FeatureObject = {
    "entities": {
        "connected": {
            "type": Platform.BINARY_SENSOR,
            "variant": "custom",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "connection_status": {
            "type": Platform.SENSOR,
            "variant": "custom",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "fan:rpm": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": None,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "fan:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "fan:duty-cycle-min": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "fan:rpm-prescaler": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "fan:vcc-pwm": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "fan:vcc-pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "fan": {
            "type": Platform.FAN,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "out-a": {
            "type": Platform.NUMBER,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "out-b": {
            "type": Platform.NUMBER,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "out-c": {
            "type": Platform.NUMBER,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "out-d": {
            "type": Platform.NUMBER,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "out-e": {
            "type": Platform.NUMBER,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "out-f": {
            "type": Platform.NUMBER,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "out-a:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-b:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-c:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-d:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-e:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-f:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-a:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
            "sensor_class": None,
        },
        "out-b:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
            "sensor_class": None,
        },
        "out-c:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
            "sensor_class": None,
        },
        "out-d:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
            "sensor_class": None,
        },
        "out-e:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
            "sensor_class": None,
        },
        "out-f:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
            "sensor_class": None,
        },
        "out-a:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-b:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-c:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-d:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-e:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-f:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-a:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-b:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-c:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-d:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-e:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-f:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-a:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-b:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-c:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-d:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-e:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-f:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-a:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-b:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-c:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-d:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-e:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-f:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-a:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-b:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-c:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-d:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-e:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "out-f:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-12v": {
            "type": Platform.SWITCH,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "switch-12v:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-24v-a:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-24v-b:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-12v:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-24v-a:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-24v-b:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-12v:duty-cycle": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-24v-a:duty-cycle": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-24v-b:duty-cycle": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-12v:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-24v-a:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-24v-b:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "switch-24v-a": {
            "type": Platform.SWITCH,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "switch-24v-b": {
            "type": Platform.SWITCH,
            "variant": "custom",
            "category": None,
            "sensor_class": None,
        },
        "in-a": {
            "type": Platform.SENSOR,
            "variant": "custom",
            "category": None,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "in-b": {
            "type": Platform.SENSOR,
            "variant": "custom",
            "category": None,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "in-a:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "in-b:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "in-a:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "in-b:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "in-a:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "in-b:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "led:verbosity": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "user-button:pressed": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "user-button:single-press-command": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "user-button:double-press-command": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "user-button:double-press-delay": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:polling": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "rs485:error": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "rs485:response": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "rs485:timeout": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:baudrate": {
            "type": Platform.SELECT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:arbitration:probe-duration": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:arbitration:probe-delay": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:arbitration:upper-threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:arbitration:lower-threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:arbitration:max-tries": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:receiver-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "rs485:driver-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "extension:metas": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "radio:teaching:timeout": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:teaching:max-candidates": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:pulse-length": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:pulse-length:s-high": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:pulse-length:s-low": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:pulse-length:0-high": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:pulse-length:0-low": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:pulse-length:1-high": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:pulse-length:1-low": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "radio:device:transmission-repetitions": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "tag": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "time:date": {
            "type": Platform.DATE,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "time:daytime": {
            "type": Platform.TIME,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "time:timezone": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "time:ntp-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "time:ntp-server": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "eeprom:checksum": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "eeprom:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "eeprom:size": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "eeprom:contains-data": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "wifi:hostname": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:access-point:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:access-point:ssid": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:access-point:key": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:access-point:ip": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "wifi:client:networks": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "wifi:client:ssid": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:client:key": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:client:rssi": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "wifi:client:persistent": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:client:ip": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "wifi:client:mac": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "wifi:client:reconnect": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:client:reconnect-interval": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:client:connected": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "wifi:incognito:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "wifi:incognito:delay": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "websocket:remote:allow-connection": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "websocket:remote:connected": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "websocket:remote:authenticated": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "websocket:remote:uid": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "websocket:remote:domain": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "websocket:remote:port": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "websocket:remote:url": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "websocket:remote:reconnect-interval": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "websocket:local-server:port": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "websocket:local-server:clients": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "websocket:local-server:client-count": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "websocket:remote-subscribers": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "subscription:period": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "user:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "user:logged-in": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "user:name": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "user:token": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "firmware:initialized": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "firmware:automatic-updates-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "firmware:version": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "firmware:target-version": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "firmware:update-server": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "firmware:backup-update-server": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "firmware:polling-period": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "firmware:polling-timeout": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "firmware:ignore-json": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "system:reset-cause": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "system:debugging-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "system:frequency": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "system:rescue-mode": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": None,
        },
        "system:heap:size": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "system:heap:free": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "system:heap:largest-block": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "system:heap:watermark": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
            "sensor_class": SensorStateClass.MEASUREMENT,
        },
        "system:serial:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "system:serial:baudrate": {
            "type": Platform.SELECT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
        "app:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
            "sensor_class": None,
        },
    }
}
