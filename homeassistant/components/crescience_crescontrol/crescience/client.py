#!/usr/local/bin/python3
"""Simple websocket-client wrapper."""
# Logging configuration
import logging as log
import ssl
from threading import Thread
from typing import Union

import websocket

from .message import Message, ParseError

log.basicConfig(level=log.INFO)
_LOGGER = log.getLogger(__name__)


DEBUG = False


class WebsocketClient:
    """A Websocket-Client, which fits to CresNet clients.

    Attributes:
        .run

    Functions:
        .start()                    Start the socket
        .stop()                     Stop the socket
        .send(msg, clientID)        Send string to server

    Callbacks:
        .received(msg)              Called, if message received
        .on_error(error)             Called on error
        .on_close()                  Called, after connection is closed
        .on_open()                   Called, after connection is opened

    Args:
        host (str): Host-Adresse of server.
            E.g. '0.0.0.0' for network, '127.0.0.1' for local
        port (int): Port
        password (str): Password used for AES-encryption
        use_ssl (bool): If true, only ssl-connection is accepted
    """

    def __init__(
        self,
        host: Union[None, str] = None,
        port: int = 80,
        password: Union[str, None] = None,
        use_ssl: bool = False,
    ) -> None:
        """Create a new Websocket client."""
        self.run = False
        self.runner: Thread | None = None
        self.ws: websocket.WebSocketApp | None = None
        self.port = port
        self.host = host
        self.use_ssl = use_ssl

        # if isinstance(self.host, str) and self.host != "":
        #     self.start(host)

    def start(
        self,
        host: Union[None, str] = None,
        port: Union[int, None] = None,
        use_ssl: Union[bool, None] = None,
    ):
        """Start the websocket connection."""
        if self.run:
            return
        if host is not None and isinstance(host, str):
            self.host = host
        if port is not None and isinstance(port, int):
            self.port = port
        if use_ssl is not None and isinstance(host, bool):
            self.use_ssl = use_ssl

        if self.use_ssl:
            prefix = "wss://"
        else:
            prefix = "ws://"

        _LOGGER.info("Starting connection with %s%s:%s", prefix, self.host, self.port)

        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            prefix + str(self.host) + ":" + str(self.port),
            on_message=self.__received,
            on_error=self.__on_error,
            on_close=self.__on_close,
        )
        self.ws.on_open = self.__on_open
        if self.use_ssl:
            sslopt = {"sslopt": {"cert_reqs": ssl.CERT_NONE}}
        else:
            sslopt = {}
        self.runner = Thread(target=self.ws.run_forever, kwargs=sslopt)
        # self.runner.daemon = True
        self.runner.daemon = False
        self.runner.start()

    def stop(self):
        """Stop the websocket connection."""
        if self.ws is None:
            return
        self.run = False
        self.ws.keep_running = False
        self.runner = None
        self.ws = None

    def send(self, msg: str):
        """Send a message to the host."""
        if self.ws is None:
            return
        # if self.crypto is not None:
        #     msg = self.crypto.encrypt(msg)

        self.ws.send(msg)

    def received(self, msg: Message):
        """User defined callback when a message is received."""
        if DEBUG:
            print_debug("Message", str(msg))

    def on_error(self, error):
        """User defined callback when connection is errored."""
        if DEBUG:
            print_debug("Error", error)

    def on_close(self):
        """User defined callback when connection is closed."""
        if DEBUG:
            print_debug("Close")

    def on_open(self):
        """User defined callback when connection is opened."""
        self.send("subscription:subscribe()")
        if DEBUG:
            print_debug("Open")

    def __on_error(self, ws, error):
        self.run = False
        if self.on_error is not None:
            self.on_error(error)

    def __on_close(self, ws, *args):
        self.run = False
        if self.on_close is not None:
            self.on_close()

    def __on_open(self, ws):
        self.run = True
        if self.on_open is not None:
            self.on_open()

    def __received(self, ws, msg: str):
        self.run = True
        # if self.crypto is not None:
        #     msg = self.crypto.decrypt(msg)
        if self.received is not None and msg is not None:
            try:
                format_msg = Message(None, [], None, None)
                format_msg.parse("fake::" + msg, True)
                # _LOGGER.info(format_msg.status())
                self.received(format_msg)
            except ParseError:
                _LOGGER.exception("Failed to parse message: %s", msg)


def print_debug(typ: Union[str, None] = None, element: Union[str, None] = None):
    """Human readable debugging information."""
    msg = f"Received: {typ}"
    if typ == "UNKNOWN":
        _LOGGER.warning(msg)
        _LOGGER.warning(element)
    elif typ == "Error":
        _LOGGER.error(msg)
        _LOGGER.error(element)
    else:
        _LOGGER.info(msg)
        _LOGGER.info(element)


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
        use_ssl=use_ssl_input,
    )

    client.received = lambda msg: _LOGGER.info("Received: %s", msg)  # type: ignore[method-assign]
    client.on_error = lambda error: _LOGGER.info("Error: %s", error)  # type: ignore[method-assign]
    client.on_close = lambda: _LOGGER.info("Connection closed")  # type: ignore[method-assign]
    client.on_open = lambda: _LOGGER.info("Connection opened")  # type: ignore[method-assign]

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
            _LOGGER.info("%s\nRunning: %s", info, str(client.run))
        elif user_input == "start":
            client.start()
        elif user_input == "stop":
            client.stop()
        elif user_input.startswith("send "):
            client.send(user_input)
        elif user_input == "exit":
            _LOGGER.info("Goodbye")
        else:
            _LOGGER.info("Unknown command")

    client.stop()
