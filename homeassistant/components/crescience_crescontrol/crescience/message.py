#!/usr/bin/env python3
"""Message and command objects for Cres-Protocol."""

import ast
import json
import logging as log
from typing import Any, Literal

log.basicConfig(level=log.INFO)
_LOGGER = log.getLogger(__name__)


def get_target(msg: str):  # , user:User=None):
    """Get target from message-string."""
    idx = msg.index(":")
    if idx == -1:
        return None
    split = msg.split(":")
    return [split[0], ":".join(split[1:])]


def check_function(
    msg, num_params=1, perspective: Literal["server"] | Literal["client"] = "server"
):
    """Check a message-string for number of arguments."""
    error = None
    try:
        msg = Message(str(msg), perspective=perspective)
        if len(msg.commands) == 0:
            error = "No command"
        params = msg.commands[0].func_parameters
        if params is None:
            error = "No arguments provided"
        elif len(params) != num_params:
            error = "Takes exactly " + str(num_params) + " arguments"
    except InvalidMessage as e:
        msg = None
        error = str(e)
    except ParseError as e:
        msg = None
        error = str(e)
    except InvalidCommand as e:
        msg = None
        error = str(e)
    return msg, error


class Command:
    """Object-representation of command."""

    def __init__(
        self,
        path: list[str] | str | None = None,
        parameters: list[Any] | None = None,
        value: Any = None,
    ) -> None:
        """Create or parse a command object."""
        self.valid = False
        self.typ: Literal[
            "parameterSet", "parameterGet", "functionCall"
        ] | None = None  # PARAMETER_SET, PARAMETER_GET, FUNCTION_CALL
        if isinstance(path, str):
            # self.path = None
            self.func_parameters: list[Any] | None = None
            self.attr_setvalue: Any = None
            self.parse(path)
        else:
            if path is None:
                self.path = []
            else:
                self.path = path
            self.func_parameters = parameters
            self.attr_setvalue = value

    def checkValidity(self):
        """Check message validity."""
        if len(self.path) == 0:
            raise InvalidCommand(f"You must specify a path: {self.path}")
        if ":" in "".join(self.path):
            raise InvalidCommand(f'No : and " allowed in the path: {self.path}')
        # if self.attr_setvalue == "":
        #     _LOGGER.error("Cannot set an empty string")
        #     return False
        return True

    def status(self):
        """Human readable status of message."""
        status = f"Typ   : {self.typ}\n"
        if self.func_parameters is not None:
            status = status + f"Function parameters: {self.func_parameters}\n"
            status = status + "Function par. Types: {}\n".format(
                str(self.functionParameterTypes)
            )
        if self.attr_setvalue is not None:
            status = status + f"Attribute setValue : {self.attr_setvalue}\n"
            status = status + "Attribute set.Types: {}\n".format(
                str(self.attributeSetValueType)
            )
        return status

    def identifyTyp(self):
        """Identify message type."""
        if self.attr_setvalue is not None and self.func_parameters is None:
            self.typ = "parameterSet"
        elif self.attr_setvalue is None and self.func_parameters is not None:
            self.typ = "functionCall"
        elif self.attr_setvalue is None and self.func_parameters is None:
            self.typ = "parameterGet"
        else:
            self.valid = False
            self.typ = None
            return None
        return self.typ

    def parse(self, strung: str):
        """Parse command from string."""
        # _LOGGER.info('Parsing command: {}'.format(strung))
        path_split = strung.split(":")
        path = path_split[:-1]
        last_element = path_split[-1]
        parameters = None
        value = None
        if "=" in last_element:
            self.typ = "parameterSet"
            split = last_element.split("=")
            value = split[1]
        elif "(" in last_element:
            self.typ = "functionCall"
            split = last_element.split("(")
            split[1] = split[1].replace(")", "")
            parameters = split[1].split(",")
        else:
            self.typ = "parameterGet"
            split = [last_element]
        path.append(split[0])

        self.path = path
        self.attr_setvalue = value
        self.func_parameters = parameters

    def resubstitute(self, subs: dict[str, str]):
        """Resubstitute strings."""
        for s in subs:
            if self.attr_setvalue is not None:
                if s in self.attr_setvalue:
                    self.attr_setvalue = self.attr_setvalue.replace(s, subs[s])
            if self.func_parameters is not None:
                for idx, p in enumerate(self.func_parameters):
                    if s in p:
                        subst_params = p.replace(s, subs[s])
                        self.func_parameters[idx] = subst_params

    def detect_types(self):
        """Detect function argument types."""
        # detect types
        if self.func_parameters is not None:
            if self.func_parameters == [""]:
                self.func_parameters = []
            else:
                for idx, p in enumerate(self.func_parameters):
                    self.func_parameters[idx] = convertAnyType(p)
        self.attr_setvalue = convertAnyType(self.attr_setvalue)

    @property
    def functionParameterTypes(self):
        """Type of function parameters. None if not a function-call."""
        if self.func_parameters is None:
            return None
        if len(self.func_parameters) == 0:
            return []
        return [type(p) for p in self.func_parameters]

    @property
    def attributeSetValueType(self):
        """Type of set-value. None if not a set-value."""
        if self.attr_setvalue is None:
            return None
        return type(self.attr_setvalue)

    def __str__(self):
        """String-representation of command."""
        msg = ""
        if len(self.path) > 0:
            msg = msg + ":".join(self.path)
        if self.func_parameters is not None:
            if len(self.func_parameters) > 0:
                msg = msg + "("
                for fun in self.func_parameters:
                    if isinstance(fun, str):
                        fun = '"' + fun + '"'
                    msg = msg + str(fun) + ","
                msg = msg[:-1] + ")"
            else:
                msg = msg + "()"
        if self.attr_setvalue is not None:
            if isinstance(self.attr_setvalue, str):
                msg = msg + '="' + str(self.attr_setvalue).replace('"', '\\"') + '"'
            else:
                msg = msg + "=" + str(self.attr_setvalue).replace("'", '"')
        return msg


class Message:
    """Message object."""

    def __init__(
        self,
        target: str | None = None,
        commands: list[Command] | None = None,
        sender: str | None = None,
        returns: list[Any] | None = None,
        perspective: Literal["server"] | Literal["client"] | None = None,
    ) -> None:
        """Message object initialization by single string or object representation."""
        if isinstance(target, str) and sender is None and commands == []:
            self.sender: str | None = None
            self.target: str | None = None
            self.commands: list[Command] = []
            self.valid: bool | None = None
            self.route: list[str] | None = None  # originClient->Server,…,
            self.returns: list[Any] | None = None
            if perspective == "server":
                is_server = False
            elif perspective == "client":
                is_server = True
            else:
                is_server = False
            # try:
            self.parse(target, is_server)
            # except Exception as error:
            #     _LOGGER.warning("Error while parsing: {}".format(error))
        else:
            self.sender = sender
            self.target = target
            if commands is not None:
                self.commands = commands
            else:
                self.commands = []
            self.valid = None
            self.route = None  # originClient->Server,…,
            self.returns = returns

    def identifyRoute(self):
        """Identification of message route."""
        if self.sender is not None and self.returns is not None:
            self.route = ["server", "originClient"]
        elif self.sender is None and self.returns is None:
            self.route = ["originClient", "server"]
        elif self.sender is not None and self.returns is None:
            self.route = ["server", "targetClient"]
        elif self.sender is None and self.returns is not None:
            self.route = ["targetClient", "server"]
        else:
            self.route = None
        return self.route

    def checkValidity(self):
        """Validity-check of object. Raises errors."""
        if self.valid:
            return self.valid
        for command in self.commands:
            if not command.checkValidity():
                self.valid = False
                return self.valid
        self.valid = self._checkValidity()
        return self.valid

    def _checkValidity(self):
        self.identifyRoute()
        if self.route is None:
            raise InvalidMessage(
                f"Communication type (route) is not valid: {self.route}"
            )
        if self.sender is not None and not isinstance(self.sender, str):
            raise InvalidMessage(f"Sender must be of type 'str': {self.sender}")
        if self.sender is not None:
            if ":" in self.sender:
                raise InvalidMessage(
                    f'No :, ", , and ; allowed in the protocol: {self.sender}'
                )
        for command in self.commands:
            typ = command.identifyTyp()
            if typ is None:
                raise InvalidMessage(f"Message type (typ) is not valid: {str(c)}")
        return True

    def status(self):
        """Human readable status-overview of message."""
        status = ""
        status = status + "---------------------------------------------------\n"
        status = status + f"Valid : {self.valid}\n"
        status = status + f"Route : {self.route}\n"
        if self.sender is not None:
            status = status + f"Sender: {self.sender}\n"
        status = status + "\n"
        status = status + f"Commands ({len(self.commands)}):"

        for command in self.commands:
            c_status = command.status()
            status = status + c_status + "\n"
            status = status + "\n"

        if self.returns is not None:
            status = status + "Returns: \n"
            for r in self.returns:
                status = status + f"Return value       : {r}\n"
                status = status + f"Return value Types : {str(type(r))}\n"
        status = status + "---------------------------------------------------"
        return status

    def reset(self):
        """Reset the message object."""
        self.valid = None
        self.route = None

    def parse(self, strung: str, is_server: bool = True):
        """Message-object from string."""
        # _LOGGER.info("Parsing message: {}".format(strung))
        self.reset()

        strung, dict_subs = substituteBetween2(
            strung,
            quote1="{",
            quote2="}",
            escape_char="\\",
            sub_prefix="<dict",
            sub_suffix=">",
        )
        strung, list_subs = substituteBetween2(
            strung,
            quote1="[",
            quote2="]",
            escape_char="\\",
            sub_prefix="<list",
            sub_suffix=">",
        )
        strung, str_subs = substituteBetween(
            strung, quotes='"', escape_char="\\", sub_prefix="<str", sub_suffix=">"
        )
        subs = {**dict_subs, **list_subs, **str_subs}
        strung = strung.replace(" ", "")
        colon_split = strung.split("::")
        if len(colon_split) == 1:
            if is_server is True:
                raise ParseError("Not possible on server")
            if is_server is None:
                _LOGGER.warning("This message is interpreted as originClient -> server")
            self.route = ["originClient", "server"]
            self.sender = None
            cmds = colon_split[0]
            rets = None
        elif len(colon_split) == 2 and (is_server is True or is_server is None):
            self.route = ["server", "targetClient"]
            self.sender = colon_split[0]
            cmds = colon_split[1]
            rets = None
        elif len(colon_split) == 2 and not is_server:
            self.route = ["targetClient", "server"]
            self.sender = None
            cmds = colon_split[0]
            rets = colon_split[1]
        elif len(colon_split) == 3:
            if is_server is False:
                raise ParseError("Not possible on client")
            if is_server is None:
                _LOGGER.warning("This message is interpreted as server -> originClient")
            self.route = ["server", "originClient"]
            self.sender = colon_split[0]
            cmds = colon_split[1]
            rets = colon_split[2]
        else:
            raise ParseError(f"Invalid number of :: splits: {len(colon_split)}")
        sender_cmds_split = cmds.split(":")
        if len(sender_cmds_split) == 0:
            raise ParseError("No target specified")

        cmds_split = ":".join(sender_cmds_split).split(";")
        if self.route[0] != "server":
            self.target = sender_cmds_split[0]
            cmds_split = ":".join(sender_cmds_split[1:]).split(";")
        # self.target = sender_cmds_split[0]
        for cmd_str in cmds_split:
            self.commands.append(Command(cmd_str))
        for command in self.commands:
            command.resubstitute(subs)
            command.detect_types()

        if rets is not None:
            retsSplit = rets.split(";")
            returns: list[float | str | dict | None] = []
            for idx, ret in enumerate(retsSplit):
                for key, sub in subs.items():
                    if key in ret:
                        retsSplit[idx] = retsSplit[idx].replace(key, sub)
                returns.append(convertAnyType(retsSplit[idx]))
            self.returns = returns

        self.checkValidity()

    def __str__(self):
        """Create string representation of message."""
        if self.valid is None:
            self.checkValidity()
        if self.valid is False:
            return ""

        msg = ""
        if self.sender is not None:
            msg = self.sender + "::"
        if self.target is not None:
            msg = msg + self.target + ":"

        for idx, command in enumerate(self.commands):
            msg = msg + str(command)

            if idx != len(self.commands) - 1:
                msg = msg + ";"

        if self.returns is not None:
            msg = msg + "::"
            for idx, r in enumerate(self.returns):
                if isinstance(r, str):
                    msg = msg + '"' + str(r).replace('"', '\\"') + '"'
                else:
                    msg = msg + str(r).replace("'", '"')

                if idx != len(self.returns) - 1:
                    msg = msg + ";"
        return msg


def convertAnyType(data: Any) -> None | float | str | dict:
    """Conversion from any type to allowed types."""
    if data is None:
        return None
    try:
        numb = float(data)
        if numb - float(int(numb)) == 0:
            numb = int(numb)
        return numb
    except ValueError:
        # try:
        #     return bool(data)
        # except:
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            try:
                return ast.literal_eval(data)
            except (SyntaxError, NameError, ValueError):
                # if isinstance(data, str):
                #     if data.startswith('"'):
                #         return data[1:-1]
                #     if data.startswith("\\"):
                #         return data[2:-2]
                return data


def substituteBetween(
    strung, quotes='"', escape_char="\\", sub_prefix="<sub", sub_suffix=">"
):
    """Substitution helper."""
    quoteIndices = [i for i, ltr in enumerate(strung) if ltr == quotes]
    return substitute(strung, quoteIndices, escape_char, sub_prefix, sub_suffix)


def substituteBetween2(
    strung: str,
    quote1="{",
    quote2="}",
    escape_char="\\",
    sub_prefix="<sub",
    sub_suffix=">",
):
    """Substitution helper."""
    quoteIndices = [
        i
        for i, ltr in enumerate(strung)
        if (
            (ltr in (quote1, quote2))
            and (strung.count('"', 0, i) - strung.count('\\"', 0, i)) % 2 == 0
        )
    ]
    if len(quoteIndices) > 0:
        pass
    return substitute(strung, quoteIndices, escape_char, sub_prefix, sub_suffix)


def substitute(
    strung: str,
    quoteIndices: list[int],
    escape_char: str,
    sub_prefix: str,
    sub_suffix: str,
):
    """Substitution of areas from a string."""
    subs: dict[str, str] = {}
    if len(quoteIndices) > 0:
        # search for \" and ignore it
        if 0 in quoteIndices:
            raise ParseError("Invalid quotes")
        escaped_quote_idxs = [i for i in quoteIndices if strung[i - 1] != escape_char]

        if len(escaped_quote_idxs) % 2 != 0:
            raise ParseError(
                f"Invalid number of quotes. Total: {len(quoteIndices)}, Unescaped: {len(escaped_quote_idxs)}"
            )

        # replace strings with placeholders
        for i in reversed(range(int(len(escaped_quote_idxs) / 2))):
            start = escaped_quote_idxs[int(i * 2)]
            end = escaped_quote_idxs[int(i * 2 + 1)] + 1
            sub = strung[start:end]
            placeholder = sub_prefix + str(len(subs)) + sub_suffix
            subs[placeholder] = sub
            strung = strung[0:start] + placeholder + strung[end:]
    return strung, subs


def checkParser(
    strung: str, perspective: Literal["server", "client"] | None = None, shouldBeOk=True
):
    """Self-check helper."""
    _LOGGER.info("\nParsing message: %s", strung)
    try:
        test = Message(strung, perspective=perspective)
    except (InvalidMessage, ParseError, InvalidCommand) as e:
        if shouldBeOk:
            _LOGGER.error("Reconstruction   Failed: %s", e)
            return 0
        _LOGGER.info("Reconstruction   Impossible: %s", e)
        return 1
    status = test.status()
    _LOGGER.info("Reconst.Message: %s", str(test))
    if str(test) == strung and shouldBeOk:
        _LOGGER.info("Reconstruction   OK")
        return 1
    if str(test) == strung and not shouldBeOk:
        _LOGGER.warning("Reconstruction   OK, but not expected!")
        return 1
    if shouldBeOk:
        _LOGGER.error("Reconstruction   [NO_ERROR] Failed!")
        _LOGGER.info(status)
        return 0
    _LOGGER.error("Reconstruction  [NO_ERROR] Impossible")
    # _LOGGER.info(status)
    return 1


if __name__ == "__main__":
    check_parse_req_server = True
    check_parse_server_req = True
    check_parse_unknown = True
    check_creation = True
    start_console = False

    _LOGGER.info("============================================================")
    _LOGGER.info("Cres-Protocol check")
    message_tests: list[tuple[str, int, int]] = [
        ('root:get-token("UID","test","user")', 0, 1),
        ("deneb-1:temperature=5", 0, 1),
        ("deneb-1:temperature=5;temperature2=5", 0, 1),
        ("deneb-1:temperature=5::6", 0, 1),
        ("deneb-1:temperature=5;temperature2=5::6", 0, 1),
        ("app-1::deneb-1:temperature=5", 1, 0),
        ("app-1::deneb-1:temperature=5;deneb-1:temperature2=5", 1, 0),
        ("app-1::deneb-1:temperature=5::6", 1, 0),
        ("app-1::deneb-1:temperature=5;deneb-1:temperature2=5::6;5", 1, 0),
        ('deneb-1:temperature="hih\\"ihi"', 0, 1),
        ('deneb-1:temperature="hih\\"ihi"::[\'Invalid\']', 0, 1),
        ('app-1::deneb-1:temperature="hih\\"ihi"', 1, 0),
        ('app-1::deneb-1:temperature="hih\\"ihi"::[\'Invalid\']', 1, 0),
        ("deneb-1:function()", 0, 1),
        ("deneb-1:function()::5", 0, 1),
        ("app-1::deneb-1:function()", 1, 0),
        ("app-1::deneb-1:function()::5", 1, 0),
        ("deneb-1:function2('wow',6)", 0, 1),
        ("deneb-1:function2('wow',6)::1", 0, 1),
        ("app-1::deneb-1:function2('wow',6)", 1, 0),
        ("app-1::deneb-1:function2('wow',6)::1", 1, 0),
        ("deneb-1:temp={'wow': 'supports', 'json': 'wow'}", 0, 1),
        ("deneb-1:temp={'wow': 'supports', 'json': 'wow'}::False", 0, 1),
        ("app-1::deneb-1:temp={'wow': 'supports', 'json': 'wow'}", 1, 0),
        ("app-1::deneb-1:temp={'wow': 'good', 'json': 'wow'}::False", 1, 0),
    ]
    message_tests = [(m[0].replace("'", '"'), m[1], m[2]) for m in message_tests]

    if check_parse_req_server:
        _LOGGER.info("============================================================")
        _LOGGER.info("Check Request-Client->Server")
        _LOGGER.info("============================================================")
        ok = 0
        for m in message_tests:
            ok += checkParser(m[0], "server", bool(m[1]))
        _LOGGER.info("%s of %s successful", ok, len(message_tests))

    if check_parse_server_req:
        _LOGGER.info("============================================================")
        _LOGGER.info("Check Server->Request-Client")
        _LOGGER.info("============================================================")
        ok = 0
        for m in message_tests:
            ok += checkParser(m[0], "client", bool(m[2]))
        _LOGGER.info("%s of %s successful", ok, len(message_tests))

    if check_parse_unknown:
        _LOGGER.info("============================================================")
        _LOGGER.info("Check None")
        _LOGGER.info("============================================================")
        ok = 0
        for m in message_tests:
            ok += checkParser(m[0], None, True)
        _LOGGER.info("%s of %s successful", ok, len(message_tests))

    if check_creation:
        _LOGGER.info("============================================================")
        _LOGGER.info("Check message creation")
        _LOGGER.info("============================================================")
        command_tests = [
            Command(path=["engine-*", "getparameter"]),
            Command(path=["engine-*", "set-parameter"], value="5zig"),
            Command(path=["engine-*", "set-parameter"], value={"w": 4}),
            Command(path=["engine-*", "set-parameter"], value=[1, 2, 3]),
            Command(path=["engine-1", "websocket", "function"], parameters=[]),
            Command(
                path=["engine-1", "websocket", "function"], parameters=[1, 2, 3, 4]
            ),
            Command(
                path=["engine-1", "websocket", "function"],
                parameters=[{"wow": 3}, 5, "boo"],
            ),
        ]
        _LOGGER.info("Commands")
        _LOGGER.info("----------------------------------------------------")

        for c in command_tests:
            _LOGGER.info(str(c))

        message_objects = [
            Message(target="deneb-1", commands=[command_tests[3]]),
            Message(target="deneb-1", commands=[command_tests[3]], sender="app-1"),
            Message(target="deneb-1", commands=[command_tests[3]], returns=[[1, 2, 3]]),
            Message(
                target="deneb-1",
                commands=[command_tests[3]],
                sender="app-1",
                returns=[[1, 2, 3]],
            ),
            Message(target="deneb-1", commands=command_tests),
            Message(target="deneb-1", commands=command_tests[3:5], sender="app-1"),
            Message(target="deneb-1", commands=command_tests[3:4], returns=[1]),
            Message(
                target="deneb-1",
                commands=command_tests[0:3],
                sender="app-1",
                returns=[1, 2, {"wow": 5}],
            ),
        ]

        _LOGGER.info("\nMessages")
        _LOGGER.info("----------------------------------------------------")
        for message in message_objects:
            _LOGGER.info(str(message))

        _LOGGER.info("\nString->Python:")
        ok = 0
        for message in message_objects:
            ok += checkParser(str(message), "server", True)
        _LOGGER.info("%s of %s successful", ok, len(message_objects))

    _LOGGER.info("\n")
    if start_console:
        cmd = ""
        perspective_test: Literal["server", "client"] | None = None
        help_string = """
Crescience Protocol v1.0
------------------------
Use this tool to parse any message

help   [h]: show help
server [s]: server-perspective (Your Client Message -> Server)
client [c]: client-perspective (Your Server Message -> Client)
none   [n]: no-perspective (No Exception - default: client-pp)
exit   [e]: Quit
"""
        _LOGGER.info(help_string)
        while cmd != "exit":
            try:
                cmd = input(f"<{perspective_test}>: ")
            except KeyboardInterrupt:
                _LOGGER.info("Aborted. To quit, enter 'exit'")
                continue
            if cmd in ("exit", "e"):
                break
            if cmd in ("help", "h"):
                _LOGGER.info(help_string)
                continue
            if cmd in ("client", "c"):
                perspective_test = "client"
                continue
            if cmd in ("server", "s"):
                perspective_test = "server"
                continue
            if cmd in ("none", "n"):
                perspective_test = None
                continue
            checkParser(cmd, perspective_test)


class ParseError(Exception):
    """Error while parsing message."""


class InvalidCommand(Exception):
    """Command object is invalid."""


class InvalidMessage(Exception):
    """Message object is invalid."""
