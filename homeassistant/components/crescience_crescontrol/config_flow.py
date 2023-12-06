"""Config flow for Crescience CresControl integration."""
from __future__ import annotations

import http.client
import logging
import socket
from typing import Any

import requests
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
    }
)


def http_command(url: str, command: str):
    """CresControl HTTP-command."""
    crescontrol = http.client.HTTPConnection(url, 80, timeout=100)
    crescontrol.request("GET", "/command?query=" + command)
    response = crescontrol.getresponse()
    crescontrol.close()
    return response.read().decode()


class PlaceholderHub:
    """Placeholder class to make tests pass.

    TODO Remove this placeholder class and replace with things from your PyPI package.
    """

    def __init__(self, host: str) -> None:
        """Initialize."""
        self.host = host

    def get_uid(self):
        """Get the device-uid using CresControl HTTP-API."""
        uid = (
            http_command(self.host, "type").replace('"', "")
            + "-"
            + http_command(self.host, "serial")
        )
        return {"uid": uid}

    def get_tag(self):
        """Get the device-tag using CresControl HTTP-API."""
        tag = http_command(self.host, "tag").replace('"', "")
        return {"tag": tag}

    def ping(self) -> bool:
        """Ping the device."""
        # test_ok = os.system("ping -c 1 " + self.host)
        get = requests.get(f"http://{self.host}", timeout=5)

        return get.status_code == 200
        # try:
        #     fp = urllib.request.urlopen(f"http://{self.host}")
        #     mybytes = fp.read()
        #     mystr = mybytes.decode("utf8")
        #     fp.close()
        #     return True
        # except Exception:
        #     return False
        # return test_ok == 0

    def tryConnect(self) -> bool:
        """Check if device is a CresControl."""
        try:
            self.get_uid()
            return True
        except socket.gaierror:
            _LOGGER.exception("Device does not respond")
            return False
        except ConnectionRefusedError:
            _LOGGER.exception("Connection refused")
            return False


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    hub = PlaceholderHub(data["host"])

    if not await hass.async_add_executor_job(hub.ping):
        raise CannotConnect

    if not await hass.async_add_executor_job(hub.tryConnect):
        raise InvalidDevice

    uid = await hass.async_add_executor_job(hub.get_uid)
    tag = await hass.async_add_executor_job(hub.get_tag)
    return {"uid": uid["uid"], "tag": tag["tag"]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Crescience CresControl."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidDevice:
                errors["base"] = "invalid_device"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                user_input["uid"] = info["uid"]
                if info["tag"] != "" and info["tag"] is not None:
                    user_input["tag"] = info["tag"]
                else:
                    user_input["tag"] = info["uid"]
                return self.async_create_entry(
                    title=user_input["tag"],
                    data=user_input,
                    description=f"IP: {user_input['host']}",
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidDevice(HomeAssistantError):
    """Error to indicate that it's not a CresNet device."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
