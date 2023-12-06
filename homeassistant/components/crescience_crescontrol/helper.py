"""Collection of helper function for entities."""
from typing import TypedDict

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass


class NumberRange(TypedDict):
    """Helper for number-entity range."""

    step: float
    min: float
    max: float


def path2nice_name(path: str):
    """Entity name for given CresControl path."""
    if path == "connection_status":
        return "Connection Status"
    path = path.replace("out-", "Output-")
    for v in ("a", "b", "c", "d", "e", "f"):
        path = path.replace(f"-{v}:", f"-{v.upper()}:")
    path = path.replace("in-", "Input-")
    path = path.replace("-", " ")
    return path.title()


def path2number_device_class(path: str):
    """Number-Entity device_class for given CresControl path."""
    if "out-" in path:
        return NumberDeviceClass.VOLTAGE
    if "timeout" in path:
        return NumberDeviceClass.DURATION


# def path2entity_category(path:str) -> EntityCategory|None:
#     if path in ("out-a","out-b","out-c","out-d","out-e","out-f","in-a","in-b") or "extension" in path:
#         return None
#     elif "enabled" in path:
#         return None
#     else:
#         return EntityCategory.CONFIG
def path2default_enabled(path: str):
    """Entity default_enabled for given CresControl path."""
    return (
        path
        in (
            "in-a",
            "in-b",
            "out-a",
            "out-b",
            "out-c",
            "out-d",
            "out-e",
            "out-f",
            "switch-12v",
            "switch-24v-a",
            "switch-24v-b",
            "fan",
            "connected",
            "system:reboot()",
            "firmware:perform-update()",
        )
        or "extension" in path
    )


def path2binary_sensor_device_class(path: str):
    """BinarySensor-Entity device_class for given CresControl path."""
    if "connected" in path or path == "connected":
        return BinarySensorDeviceClass.CONNECTIVITY
    if "enabled" in path:
        return BinarySensorDeviceClass.RUNNING
    if "temperature" in path:
        return BinarySensorDeviceClass.HEAT
    if "humidity" in path:
        return BinarySensorDeviceClass.MOISTURE
    if "voltage" in path:
        return BinarySensorDeviceClass.POWER
    if path in ("in-a", "in-b"):
        return BinarySensorDeviceClass.POWER
    return None


def path2sensor_device_class(path: str):
    """Sensor-Entity device_class for given CresControl path."""
    if "temperature" in path:
        return SensorDeviceClass.TEMPERATURE
    if "humidity" in path:
        return SensorDeviceClass.HUMIDITY
    if "voltage" in path:
        return SensorDeviceClass.VOLTAGE
    if path in ("in-a", "in-b"):
        return SensorDeviceClass.VOLTAGE
    if "system:frequency" in path:
        return SensorDeviceClass.FREQUENCY
    if "fan:rpm" in path:
        return SensorDeviceClass.FREQUENCY
    if "heap" in path:
        return SensorDeviceClass.DATA_SIZE
    if "air-pressure" in path:
        return SensorDeviceClass.PRESSURE
    if "time:daytime" in path:
        return SensorDeviceClass.TIMESTAMP
    if "rssi" in path:
        return SensorDeviceClass.SIGNAL_STRENGTH
    return None


def path2select_options(path: str) -> list[str]:
    """Select-Entity options for given CresControl path."""
    if path.endswith("baudrate"):
        rates = [
            110,
            300,
            600,
            1200,
            2400,
            4800,
            9600,
            14400,
            19200,
            38400,
            57600,
            115200,
            128000,
            256000,
        ]
        return [str(r) for r in rates]
    return []


def path2text_pattern(path: str) -> str | None:
    """Text-Entity pattern for given CresControl path."""
    if path in (
        "time:ntp-server",
        "websocket:remote:domain",
        "firmware:backup-update-server",
    ):
        # a domain
        return r"^(((([A-Za-z0-9]+){1,63}\.)|(([A-Za-z0-9]+(\-)+[A-Za-z0-9]+){1,63}\.))+){1,255}$"
    if path in ("firmware:target-version"):
        return r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    return None


def path2number_range(path: str) -> NumberRange:
    """Number-Entity range and step for given CresControl path."""
    if path in ("out-a", "out-b", "out-c", "out-d", "out-e", "out-f"):
        return {"min": 0, "max": 10, "step": 0.1}
    if path in ("led-verbosity"):
        return {"min": 0, "max": 3, "step": 1}
    if path in (
        "user-button:double-press-delay",
        "radio:teaching:timeout",
        "rs485:timeout",
        "firmware:polling-timeout",
        "firmware:polling-period",
    ):
        return {"min": 0, "max": 1000, "step": 1}
    if path in (
        "rs485:arbitration:probe-duration",
        "rs485:arbitration:probe-delay",
        "rs485:arbitration:upper-threshold",
        "rs485:arbitration:lower-threshold",
    ):
        return {"min": 0, "max": 100, "step": 1}
    if path in ("time:timezone"):
        return {"min": 0, "max": 24, "step": 0.25}
    if path in ("wifi:incognito:delay", "subscription:period"):
        return {"min": 0, "max": 10000, "step": 10}
    if path.endswith("port"):
        return {"min": 0, "max": 65535, "step": 1}
    return {"min": 0, "max": 10, "step": 1}


def path2icon(path: str):
    """Entity icon for given CresControl path."""
    if "temperature" in path:
        return "mdi:thermometer"
    if "humidity" in path:
        return "mdi:water-percent"
    if "voltage" in path:
        return "mdi:flash-triangle-outline"
    if path in ("out-a", "out-b", "out-c", "out-d", "out-e", "out-f"):
        return "mdi:flash-triangle-outline"
    if "system:frequency" in path:
        return "mdi:cpu-32-bit"
    if "fan:rpm" in path:
        return "mdi:fan"
    if "heap" in path:
        return "mdi:memory"
    if path in ("time:daytime"):
        return "mdi:clock-time-eight"
    if "rssi" in path:
        return "mdi:wifi-strength-1"
    return None


def path2unit(path: str):
    """Entity unit for given CresControl path."""
    if "temperature" in path:
        return "°C"
    if "humidity" in path:
        return "%"
    if "voltage" in path:
        return "V"
    if path in ("out-a", "out-b", "out-c", "out-d", "out-e", "out-f", "in-a", "in-b"):
        return "V"
    if "system:frequency" in path:
        return "MHz"
    if "fan:rpm" in path:
        return "Hz"
    if "heap" in path:
        return "kByte"
    if "air-pressure" in path:
        return "kPa"
    if "time:daytime" in path:
        return ""
    if "rssi" in path:
        return "dB"
    return None


def parseBool(value: str):
    """Parse string to bool."""
    return value.lower() in [
        "true",
        "1",
        "t",
        "y",
        "yes",
        "yeah",
        "yup",
        "certainly",
        "uh-huh",
    ]
