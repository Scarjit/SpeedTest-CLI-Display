import json
import glob
import os
from tabulate import tabulate
import humanize

def main():
    tests = []
    for file in glob.glob("*.json"):
        splits = file.replace(".json", '').split("_")
        test = None
        with open(file, "r") as f:
            test = speed_test_from_dict(json.load(f))

            tests.append([
                splits[0],
                splits[1],
                f"{humanize.naturalsize(test.download/8)}/s",
                f"{humanize.naturalsize(test.upload/8)}/s",
                f"{test.ping} ms"
            ])
    print(tabulate(tests, headers=["Location", "Network", "Download", "Upload", "Ping"], tablefmt='fancy_grid'))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Client:
    ip: str
    lat: str
    lon: str
    isp: str
    isprating: str
    rating: int
    ispdlavg: int
    ispulavg: int
    loggedin: int
    country: str

    @staticmethod
    def from_dict(obj: Any) -> 'Client':
        assert isinstance(obj, dict)
        ip = from_str(obj.get("ip"))
        lat = from_str(obj.get("lat"))
        lon = from_str(obj.get("lon"))
        isp = from_str(obj.get("isp"))
        isprating = from_str(obj.get("isprating"))
        rating = int(from_str(obj.get("rating")))
        ispdlavg = int(from_str(obj.get("ispdlavg")))
        ispulavg = int(from_str(obj.get("ispulavg")))
        loggedin = int(from_str(obj.get("loggedin")))
        country = from_str(obj.get("country"))
        return Client(ip, lat, lon, isp, isprating, rating, ispdlavg, ispulavg, loggedin, country)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ip"] = from_str(self.ip)
        result["lat"] = from_str(self.lat)
        result["lon"] = from_str(self.lon)
        result["isp"] = from_str(self.isp)
        result["isprating"] = from_str(self.isprating)
        result["rating"] = from_str(str(self.rating))
        result["ispdlavg"] = from_str(str(self.ispdlavg))
        result["ispulavg"] = from_str(str(self.ispulavg))
        result["loggedin"] = from_str(str(self.loggedin))
        result["country"] = from_str(self.country)
        return result


@dataclass
class Server:
    url: str
    lat: str
    lon: str
    name: str
    country: str
    cc: str
    sponsor: str
    id: int
    host: str
    d: float
    latency: float

    @staticmethod
    def from_dict(obj: Any) -> 'Server':
        assert isinstance(obj, dict)
        url = from_str(obj.get("url"))
        lat = from_str(obj.get("lat"))
        lon = from_str(obj.get("lon"))
        name = from_str(obj.get("name"))
        country = from_str(obj.get("country"))
        cc = from_str(obj.get("cc"))
        sponsor = from_str(obj.get("sponsor"))
        id = int(from_str(obj.get("id")))
        host = from_str(obj.get("host"))
        d = from_float(obj.get("d"))
        latency = from_float(obj.get("latency"))
        return Server(url, lat, lon, name, country, cc, sponsor, id, host, d, latency)

    def to_dict(self) -> dict:
        result: dict = {}
        result["url"] = from_str(self.url)
        result["lat"] = from_str(self.lat)
        result["lon"] = from_str(self.lon)
        result["name"] = from_str(self.name)
        result["country"] = from_str(self.country)
        result["cc"] = from_str(self.cc)
        result["sponsor"] = from_str(self.sponsor)
        result["id"] = from_str(str(self.id))
        result["host"] = from_str(self.host)
        result["d"] = to_float(self.d)
        result["latency"] = to_float(self.latency)
        return result


@dataclass
class SpeedTest:
    download: float
    upload: float
    ping: float
    server: Server
    timestamp: datetime
    bytes_sent: int
    bytes_received: int
    share: None
    client: Client

    @staticmethod
    def from_dict(obj: Any) -> 'SpeedTest':
        assert isinstance(obj, dict)
        download = from_float(obj.get("download"))
        upload = from_float(obj.get("upload"))
        ping = from_float(obj.get("ping"))
        server = Server.from_dict(obj.get("server"))
        timestamp = from_datetime(obj.get("timestamp"))
        bytes_sent = from_int(obj.get("bytes_sent"))
        bytes_received = from_int(obj.get("bytes_received"))
        share = from_none(obj.get("share"))
        client = Client.from_dict(obj.get("client"))
        return SpeedTest(download, upload, ping, server, timestamp, bytes_sent, bytes_received, share, client)

    def to_dict(self) -> dict:
        result: dict = {}
        result["download"] = to_float(self.download)
        result["upload"] = to_float(self.upload)
        result["ping"] = to_float(self.ping)
        result["server"] = to_class(Server, self.server)
        result["timestamp"] = self.timestamp.isoformat()
        result["bytes_sent"] = from_int(self.bytes_sent)
        result["bytes_received"] = from_int(self.bytes_received)
        result["share"] = from_none(self.share)
        result["client"] = to_class(Client, self.client)
        return result


def speed_test_from_dict(s: Any) -> SpeedTest:
    return SpeedTest.from_dict(s)


def speed_test_to_dict(x: SpeedTest) -> Any:
    return to_class(SpeedTest, x)

if __name__ == '__main__':
    main()
