"""Definition of CresControl hardware/software variants."""
import logging
from typing import Literal, TypedDict

from homeassistant.const import EntityCategory, Platform

_LOGGER = logging.getLogger(__name__)


class EntityDefinition(TypedDict):
    """Definition of a CresControl entity."""

    type: Platform
    variant: Literal["simple", "custom"]
    category: EntityCategory | None


class FeatureObject(TypedDict):
    """Definition of CresControl entities."""

    entities: dict[str, EntityDefinition]


STATIC_CRESCONTROL_FEATURES: FeatureObject = {
    "entities": {
        "connected": {
            "type": Platform.BINARY_SENSOR,
            "variant": "custom",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "connection_status": {
            "type": Platform.SENSOR,
            "variant": "custom",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "fan:rpm": {"type": Platform.SENSOR, "variant": "simple", "category": None},
        "fan:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "fan:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "fan:duty-cycle-min": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "fan:rpm-prescaler": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "fan:vcc-pwm": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "fan:vcc-pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "fan": {"type": Platform.FAN, "variant": "custom", "category": None},
        "out-a": {"type": Platform.NUMBER, "variant": "custom", "category": None},
        "out-b": {"type": Platform.NUMBER, "variant": "custom", "category": None},
        "out-c": {"type": Platform.NUMBER, "variant": "custom", "category": None},
        "out-d": {"type": Platform.NUMBER, "variant": "custom", "category": None},
        "out-e": {"type": Platform.NUMBER, "variant": "custom", "category": None},
        "out-f": {"type": Platform.NUMBER, "variant": "custom", "category": None},
        "out-a:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-b:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-c:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-d:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-e:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-f:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-a:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
        },
        "out-b:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
        },
        "out-c:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
        },
        "out-d:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
        },
        "out-e:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
        },
        "out-f:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": None,
        },
        "out-a:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-b:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-c:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-d:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-e:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-f:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-a:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-b:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-c:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-d:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-e:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-f:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-a:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-b:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-c:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-d:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-e:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-f:threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-a:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-b:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-c:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-d:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-e:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-f:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-a:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-b:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-c:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-d:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-e:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "out-f:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-12v": {"type": Platform.SWITCH, "variant": "custom", "category": None},
        "switch-12v:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-24v-a:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-24v-b:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-12v:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-24v-a:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-24v-b:pwm-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-12v:duty-cycle": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-24v-a:duty-cycle": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-24v-b:duty-cycle": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-12v:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-24v-a:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-24v-b:pwm-frequency": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "switch-24v-a": {
            "type": Platform.SWITCH,
            "variant": "custom",
            "category": None,
        },
        "switch-24v-b": {
            "type": Platform.SWITCH,
            "variant": "custom",
            "category": None,
        },
        "in-a": {"type": Platform.SENSOR, "variant": "custom", "category": None},
        "in-b": {"type": Platform.SENSOR, "variant": "custom", "category": None},
        "in-a:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "in-b:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "in-a:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "in-b:calib-offset": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "in-a:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "in-b:calib-factor": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "led:verbosity": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "user-button:pressed": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "user-button:single-press-command": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "user-button:double-press-command": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "user-button:double-press-delay": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:polling": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "rs485:error": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "rs485:response": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "rs485:timeout": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:baudrate": {
            "type": Platform.SELECT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:arbitration:probe-duration": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:arbitration:probe-delay": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:arbitration:upper-threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:arbitration:lower-threshold": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:arbitration:max-tries": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:receiver-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "rs485:driver-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "extension:metas": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "radio:teaching:timeout": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:teaching:max-candidates": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:pulse-length": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:pulse-length:s-high": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:pulse-length:s-low": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:pulse-length:0-high": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:pulse-length:0-low": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:pulse-length:1-high": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:pulse-length:1-low": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "radio:device:transmission-repetitions": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "tag": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "time:date": {
            "type": Platform.DATE,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "time:daytime": {
            "type": Platform.TIME,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "time:timezone": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "time:ntp-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "time:ntp-server": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "eeprom:checksum": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "eeprom:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "eeprom:size": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "eeprom:contains-data": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "wifi:hostname": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:access-point:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:access-point:ssid": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:access-point:key": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:access-point:ip": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "wifi:client:networks": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "wifi:client:ssid": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:client:key": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:client:rssi": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "wifi:client:persistent": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:client:ip": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "wifi:client:mac": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "wifi:client:reconnect": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:client:reconnect-interval": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:client:connected": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "wifi:incognito:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "wifi:incognito:delay": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "websocket:remote:allow-connection": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "websocket:remote:connected": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "websocket:remote:authenticated": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "websocket:remote:uid": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "websocket:remote:domain": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "websocket:remote:port": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "websocket:remote:url": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "websocket:remote:reconnect-interval": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "websocket:local-server:port": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "websocket:local-server:clients": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "websocket:local-server:client-count": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "websocket:remote-subscribers": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "subscription:period": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "user:state": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "user:logged-in": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "user:name": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "user:token": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "firmware:initialized": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "firmware:automatic-updates-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "firmware:version": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "firmware:target-version": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "firmware:update-server": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "firmware:backup-update-server": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "firmware:polling-period": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "firmware:polling-timeout": {
            "type": Platform.NUMBER,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "firmware:ignore-json": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "system:reset-cause": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "system:debugging-enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "system:frequency": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "system:rescue-mode": {
            "type": Platform.BINARY_SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "system:heap:size": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "system:heap:free": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "system:heap:largest-block": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "system:heap:watermark": {
            "type": Platform.SENSOR,
            "variant": "simple",
            "category": EntityCategory.DIAGNOSTIC,
        },
        "system:serial:enabled": {
            "type": Platform.SWITCH,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "system:serial:baudrate": {
            "type": Platform.SELECT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
        "app:meta": {
            "type": Platform.TEXT,
            "variant": "simple",
            "category": EntityCategory.CONFIG,
        },
    }
}
