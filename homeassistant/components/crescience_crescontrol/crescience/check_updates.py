"""Functions to get versions from Crescience update servers."""
from html.parser import HTMLParser
import logging
import pprint
from typing import TypedDict

import requests

_LOGGER = logging.getLogger(__name__)

pprinter = pprint.PrettyPrinter()


class ApacheDirectory(TypedDict):
    """Structure of an apache directory."""

    files: list[str]
    folders: list[str]


class VersionInfo(TypedDict):
    """Structure of an apache directory."""

    version: str
    version_dir: str
    real_version: str
    release_data: str
    device: str
    change_log: str
    size: str
    install: bool
    data: list[str]
    summary: str


class ApacheDirectoryParser(HTMLParser):
    """HTML Parser for Apache directories."""

    _is_link = False
    folders: list[str] = []
    files: list[str] = []

    def __init__(self) -> None:
        """HTML Parser for Apache directories."""
        super().__init__()
        self.folders = []
        self.files = []
        self._is_link = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        """Extract links to subdirectories and."""
        self._is_link = tag == "a"
        for attr in attrs:
            if (
                attr[0] == "href"
                and attr[1] is not None
                and not attr[1].startswith("?")
                and attr[1] != "/"
                and attr[1] not in self.folders
            ):
                if attr[1].endswith("/"):
                    self.folders.append(attr[1])
                else:
                    self.files.append(attr[1])

    @property
    def result(self) -> ApacheDirectory:
        """Return structure of parsed Apache directory."""
        return {"folders": self.folders, "files": self.files}

    # def handle_endtag(self, tag: str):
    #     print("Encountered an end tag :", tag)

    # def handle_data(self, data):
    #     print("Encountered some data  :", data)


def parse_apache_index(host: str, url: str, port=443):
    """Parse Apache index web-page."""
    # connection = http.client.HTTPConnection(host, port, timeout=100)
    # connection.request("GET", url)
    # response = connection.getresponse()
    # connection.close()
    # return response.read().decode()
    schema = "https://" if port == 443 else "http://"
    body = requests.get(schema + host + url, timeout=5)
    parser = ApacheDirectoryParser()
    parser.feed(body.text)
    return parser.result


def get_version_info(url: str, port=443):
    """Parse info of version.json ."""
    schema = "https://" if port == 443 else "http://"
    body = requests.get(schema + url, timeout=5)
    return body.json()


def update_server_online(url: str, port=443) -> bool:
    """Ping the device."""
    schema = "https://" if port == 443 else "http://"
    get = requests.get(schema + url, timeout=5)
    return get.status_code == 200


def get_available_versions(
    url="update.cre.science", device_type="crescontrol", port=443
):
    """Get available firmware versions from Crescience Update-Server."""
    online = update_server_online(url, port)
    if not online:
        _LOGGER.warning("Crescience Update-Server at %s is offline", url)
        raise ConnectionError(f"Crescience Update-Server at {url} is offline")
    _LOGGER.info("Crescience Update-Server at %s is online", url)
    base_folder = parse_apache_index(url, f"/{device_type}", port)
    available_versions: list[VersionInfo] = []
    for folder in base_folder["folders"]:
        version_folder = parse_apache_index(url, f"/{device_type}/{folder}", port)
        if "info.json" in version_folder["files"]:
            data = get_version_info(f"{url}/{device_type}/{folder}/info.json", port)
            data["version_dir"] = folder
            data["real_version"] = folder.replace(
                "version-", data["version"] + "+"
            ).replace("/", "")
            data[
                "summary"
            ] = f"Changelog: {data['change_log']}. Release-Date: {data['release_date']}. Size: {data['size']}"
            available_versions.append(data)
    return available_versions


def get_latest_version(url="update.cre.science", device_type="crescontrol", port=443):
    """Get latest version. Assumes, that the last folder is the latest version."""
    available_versions = get_available_versions(url, device_type, port)
    return available_versions[-1]


if __name__ == "__main__":
    versions = get_available_versions("update.cre.science")
    nightly_versions = get_available_versions("update-nightly.cre.science")
    pprinter.pprint(versions)
    pprinter.pprint(nightly_versions)
