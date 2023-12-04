#!/usr/local/bin/python3
"""Simple websocket-client wrapper."""
import asyncio
from collections.abc import Callable
from enum import IntEnum, StrEnum
import logging
from typing import Literal, Union

import aiohttp

from .message import Message, ParseError

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

MAX_FAILED_ATTEMPTS = 5


class ConnectionState(StrEnum):
    """State of the Websocket connection."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    STARTING = "starting"
    STOPPED = "stopped"


class ConnectionMessageType(IntEnum):
    """Message type for websocket callback."""

    # websocket spec types
    # CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    # PING = 0x9
    # PONG = 0xA
    # CLOSE = 0x8

    # aiohttp specific types
    # CLOSING = 0x100
    CLOSED = 0x101
    ERROR = 0x102
    OPEN = 0x105


class ConnectionErrorReason(StrEnum):
    """Error reasons of the Websocket connection."""

    ERROR_AUTH_FAILURE = "Authorization failure"
    ERROR_TOO_MANY_RETRIES = "Too many retries"
    ERROR_UNKNOWN = "Unknown"


class WebsocketClient:
    """A Websocket-Client, which fits to CresNet clients."""

    def __init__(
        self,
        host: str,
        port: int = 80,
        password: Union[str, None] = None,
        verify_ssl: bool = False,
        callback: Callable[
            [ConnectionMessageType, str | None, ConnectionErrorReason | None], None
        ]
        | None = None,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Create a new Websocket client."""
        self.session = session or aiohttp.ClientSession()
        self.port = port
        self.host = host
        self.callback = callback
        self.ws_client: aiohttp.ClientWebSocketResponse | None = None
        self.message_queue: list[str] = []
        self._ssl: Literal[False] | None = False if verify_ssl is False else None
        self._state: ConnectionState = ConnectionState.DISCONNECTED
        self.failed_attempts = 0
        self._error_reason: ConnectionErrorReason | None = None

    @property
    def uri(self):
        """Websocket connection URI."""
        if self._ssl:
            prefix = "wss://"
        else:
            prefix = "ws://"
        return prefix + str(self.host) + ":" + str(self.port)

    @property
    def state(self):
        """Return the current state."""
        return self._state

    @state.setter
    def state(self, value: ConnectionState):
        """Set the state."""
        self._state = value
        _LOGGER.debug("Websocket %s", value)
        if value in (
            ConnectionState.DISCONNECTED,
            ConnectionState.STARTING,
            ConnectionState.STOPPED,
        ):
            self.ws_client = None
        self._error_reason = None

    async def running(self):
        """Open a persistent websocket connection and act on events."""
        self.state = ConnectionState.STARTING

        try:
            async with self.session.ws_connect(
                self.uri, heartbeat=15, ssl=self._ssl
            ) as ws_client:
                if self.ws_client is None:
                    self.ws_client = ws_client
                if self.state != ConnectionState.CONNECTED:
                    self.state = ConnectionState.CONNECTED
                    await self._callback(ConnectionMessageType.OPEN, None, None, None)
                self.failed_attempts = 0

                async for message in ws_client:
                    if self.state == ConnectionState.STOPPED:
                        break

                    if message.type == aiohttp.WSMsgType.TEXT:
                        await self._callback(
                            ConnectionMessageType.TEXT, str(message.data), None, None
                        )

                    elif message.type == aiohttp.WSMsgType.CLOSED:
                        _LOGGER.warning("AIOHTTP websocket connection closed")
                        await self._callback(
                            ConnectionMessageType.CLOSED, None, None, None
                        )
                        break

                    elif message.type == aiohttp.WSMsgType.ERROR:
                        _LOGGER.error("AIOHTTP websocket error")
                        await self._callback(
                            ConnectionMessageType.ERROR,
                            None,
                            ConnectionErrorReason.ERROR_UNKNOWN,
                            "AIOHTTP websocket error",
                        )
                        break

        except aiohttp.ClientResponseError as error:
            if error.code == 401:
                _LOGGER.error("Credentials rejected: %s", error)
                self._error_reason = ConnectionErrorReason.ERROR_AUTH_FAILURE
                await self._callback(
                    ConnectionMessageType.ERROR,
                    None,
                    self._error_reason,
                    f"Credentials rejected: {error}",
                )
            else:
                _LOGGER.error("Unexpected response received: %s", error)
                self._error_reason = ConnectionErrorReason.ERROR_UNKNOWN
                await self._callback(
                    ConnectionMessageType.ERROR,
                    None,
                    self._error_reason,
                    f"Unexpected response received: {error}",
                )
            self.state = ConnectionState.STOPPED
        except (aiohttp.ClientConnectionError, asyncio.TimeoutError) as error:
            if self.failed_attempts >= MAX_FAILED_ATTEMPTS:
                self._error_reason = ConnectionErrorReason.ERROR_TOO_MANY_RETRIES
                self.state = ConnectionState.STOPPED
                await self._callback(
                    ConnectionMessageType.ERROR,
                    None,
                    self._error_reason,
                    f"Websocket connection timeout: {error}",
                )
            elif self.state != ConnectionState.STOPPED:
                retry_delay = min(2 ** (self.failed_attempts - 1) * 30, 300)
                self.failed_attempts += 1
                _LOGGER.error(
                    "Websocket connection failed, retrying in %ds: %s",
                    retry_delay,
                    error,
                )
                self.state = ConnectionState.DISCONNECTED
                await asyncio.sleep(retry_delay)
        except Exception as error:  # pylint: disable=broad-except
            if self.state != ConnectionState.STOPPED:
                _LOGGER.exception("Unexpected exception occurred: %s", error)
                self._error_reason = ConnectionErrorReason.ERROR_UNKNOWN
                self.state = ConnectionState.STOPPED
                await self._callback(
                    ConnectionMessageType.ERROR,
                    None,
                    self._error_reason,
                    f"Unexpected exception occurred: {error}",
                )
        else:
            if self.state != ConnectionState.STOPPED:
                self.state = ConnectionState.DISCONNECTED
                await self._callback(ConnectionMessageType.CLOSED, None, None, None)

                await asyncio.sleep(5)

    async def _callback(
        self,
        msg_type: ConnectionMessageType,
        msg: str | None,
        error: ConnectionErrorReason | None,
        error_info: str | None,
    ):
        if self.callback:
            self.callback(msg_type, msg, error)
        elif msg_type == ConnectionMessageType.ERROR:
            assert error_info is not None
            await self.__on_error(error_info)
        elif msg_type == ConnectionMessageType.TEXT:
            assert msg is not None
            await self.__received(msg)
        elif msg_type == ConnectionMessageType.CLOSED:
            await self.__on_close()
        elif msg_type == ConnectionMessageType.OPEN:
            await self.__on_open()

    async def listen(self):
        """Close the listening websocket."""
        self.failed_attempts = 0
        while self.state != ConnectionState.STOPPED:
            await self.running()

    def start(self):
        """Start synchron listening."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())

    def close(self):
        """Close the listening websocket."""
        self.state = ConnectionState.STOPPED

    async def _send_queue(self):
        if len(self.message_queue) > 0 and self.ws_client:
            for m in self.message_queue:
                await self.ws_client.send_str(m)
            self.message_queue = []

    async def send(self, msg: str):
        """Send a message to the host."""
        if self.state != ConnectionState.CONNECTED or self.ws_client is None:
            self.message_queue.append(msg)
            _LOGGER.warning(
                "Cannot send message. Websocket connection not open. Message will be queued"
            )
        else:
            await self._send_queue()
            await self.ws_client.send_str(msg)

    async def received(self, msg: Message):
        """User defined callback when a message is received."""
        _LOGGER.debug("Websocket message received")

    async def on_error(self, error: str):
        """User defined callback when connection is errored."""
        _LOGGER.debug("Websocket connection error")

    async def on_close(self):
        """User defined callback when connection is closed."""
        _LOGGER.debug("Websocket connection closed")

    async def on_open(self):
        """User defined callback when connection is opened."""
        _LOGGER.debug("Websocket connection opened")

    async def __on_error(self, error: str):
        if self.on_error is not None:
            await self.on_error(error)

    async def __on_close(self):
        if self.on_close is not None:
            await self.on_close()

    async def __on_open(self):
        if self.on_open is not None:
            await self.on_open()
        if self.ws_client:
            await self._send_queue()

    async def __received(self, msg: str):
        if self.received is not None and msg is not None:
            try:
                format_msg = Message(None, [], None, None)
                format_msg.parse("fake::" + msg, True)
                # _LOGGER.info(format_msg.status())
                await self.received(format_msg)
            except ParseError:
                _LOGGER.exception("Failed to parse message: %s", msg)


if __name__ == "__main__":
    _LOGGER.info("\n\n")
    hostname_input = input("Enter a hostname (e.g. root.cre.science): ")
    if hostname_input == "":
        hostname_input = "root.cre.science"
    port_input: int | None = None
    while port_input is None:
        portStr = input("Enter a port (e.g. 443): ")
        if portStr == "":
            port_input = 443
        else:
            try:
                port_input = int(portStr)
            except ValueError:
                port_input = None
    password_input: str | None = input("Enter password (optional): ")
    if password_input == "":
        password_input = None
    use_ssl_input = input("Is SSL-encrypted? (Y/n)") != "n"
    client = WebsocketClient(
        host=hostname_input,
        port=port_input,
        password=password_input,
        verify_ssl=use_ssl_input,
    )

    # client.start()
    _LOGGER.info("\n\n")

    info = "start: Start server\n\
            stop: Stop server\n\
            send $id $msg: Send message to client\n"
    _LOGGER.info(info)
    user_input = ""
    while user_input != "exit":
        user_input = input('Enter "exit" to stop server, "info" for information\n')

        if user_input == "info":
            _LOGGER.info("%s\nState: %s", info, str(client.state))
        elif user_input == "start":
            asyncio.run(client.listen())
        elif user_input == "stop":
            client.close()
        elif user_input.startswith("send "):
            asyncio.run(client.send(user_input))
        elif user_input == "exit":
            _LOGGER.info("Goodbye")
        else:
            _LOGGER.info("Unknown command")

    client.close()
