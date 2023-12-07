"""Functions to get versions from Crescience update servers."""
from html.parser import HTMLParser
import logging
import pprint
from typing import TypedDict

import requests

_LOGGER = logging.getLogger(__name__)

pprinter = pprint.PrettyPrinter()


class IndexEntry(TypedDict):
    """Structure of an apache index entry."""

    url: str
    last_modified: str | None


class ApacheDirectory(TypedDict):
    """Structure of an apache directory."""

    files: list[IndexEntry]
    folders: list[IndexEntry]
    dir: list[str]


class VersionInfo(TypedDict):
    """Structure of an apache directory."""

    version: str
    version_dir: str
    last_modified: str
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
    folders: list[IndexEntry] = []
    files: list[IndexEntry] = []
    _added_data: list[str] = []

    def __init__(self) -> None:
        """HTML Parser for Apache directories."""
        super().__init__()
        self._added_data = []
        self.folders = []
        self.files = []
        # self._is_link = False
        self._last_was_file = False
        self._is_last_modified_data = False
        # self.last_modified = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        """Extract links to subdirectories and."""
        # self._is_link = tag == "a"
        for attr in attrs:
            if (
                attr[0] == "href"
                and attr[1] is not None
                and not attr[1].startswith("?")
                and attr[1] != "/"
                and attr[1] not in self._added_data
            ):
                entry: IndexEntry = {"url": attr[1], "last_modified": None}
                self._added_data.append(attr[1])
                if attr[1].endswith("/"):
                    self._last_was_file = False
                    self.folders.append(entry)
                else:
                    self._last_was_file = True
                    self.files.append(entry)
            elif attr[0] == "class" and attr[1] == "indexcollastmod":
                self._is_last_modified_data = True

    @property
    def result(self) -> ApacheDirectory:
        """Return structure of parsed Apache directory."""
        return {"folders": self.folders, "files": self.files, "dir": self._added_data}

    # def handle_endtag(self, tag: str):
    #     print("Encountered an end tag :", tag)

    def handle_data(self, data):
        """Extract last-modified date."""
        if self._is_last_modified_data:
            if data not in ("", "Last modified", " ", " "):
                if self._last_was_file:
                    self.files[-1]["last_modified"] = data.strip()
                else:
                    self.folders[-1]["last_modified"] = data.strip()
            self._is_last_modified_data = False


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
        version_folder = parse_apache_index(
            url, f"/{device_type}/{folder['url']}", port
        )
        if "info.json" in version_folder["dir"]:
            data = get_version_info(
                f"{url}/{device_type}/{folder['url']}/info.json", port
            )
            data["version_dir"] = folder["url"]
            data["real_version"] = (
                folder["url"]
                .replace("version-", data["version"] + "+")
                .replace("/", "")
            )
            data["last_modified"] = folder["last_modified"]
            data[
                "summary"
            ] = f"Changelog: {data['change_log']}. Release-Date: {data['last_modified']}. Size: {data['size']}"
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
