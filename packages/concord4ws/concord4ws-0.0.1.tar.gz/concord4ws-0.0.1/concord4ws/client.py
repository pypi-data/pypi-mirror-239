#!/usr/bin/env python

import asyncio
from enum import StrEnum
from typing import Callable
from websockets.client import connect
import json


class Concord4ZoneStatus(StrEnum):
    NORMAL = "normal"
    TRIPPED = "tripped"
    FAULTED = "faulted"
    ALARM = "alarm"
    TROUBLE = "trouble"
    BYPASSED = "bypassed"
    UNKNOWN = "unknown"


class Concord4ZoneType(StrEnum):
    HARDWIRED = "hardwired"
    RF = "rf"
    TOUCHPAD = "touchpad"


class Concord4PartitionArmingLevel(StrEnum):
    OFF = "off"
    STAY = "stay"
    AWAY = "away"
    PHONE_TEST = "phone_test"
    SENSOR_TEST = "sensor_test"


class Concord4Panel:
    def __init__(self):
        self.panel_type = None


class Concord4Zone:
    def __init__(self, zone):
        self.id: str = zone["id"]
        self.partition_number: int = zone["partitionNumber"]
        self.area_number: int = zone["areaNumber"]
        self.group_number: int = zone["groupNumber"]
        self.zone_number: int = zone["zoneNumber"]
        self.zone_type: str = zone["zoneType"]
        self.zone_status: str = zone["zoneStatus"]
        self.zone_text: str = zone["zoneText"].strip().title()


class Concord4Partition:
    def __init__(self, partition):
        self.id: str = partition["id"]
        self.partition_number: int = partition["partitionNumber"]
        self.area_number: int = partition["areaNumber"]
        self.arming_level: str = partition["armingLevel"]


class Concord4State:
    def __init__(self):
        self.panel = Concord4Panel()
        self.zones = dict[str, Concord4Zone]()
        self.partitions = dict[str, Concord4Partition]()
        self.initialized = False


class Concord4WSClient:
    _connected: bool = False
    _connect_attempt: int = 0

    def __init__(self, host: str, port: str | int):
        self.host = host
        self.port = port
        self._callbacks = dict[str, set]()
        self._loop = asyncio.get_event_loop()
        self._state = Concord4State()

    @property
    def state(self):
        return self._state

    @property
    def connected(self):
        return self._connected

    async def test_connect(self) -> bool:
        try:
            async with connect(f"ws://{self.host}:{self.port}"):
                return True
        except:
            return False

    async def _event_loop(self):
        async for websocket in connect(f"ws://{self.host}:{self.port}"):
            try:
                self._connected = True
                self._connect_attempt = 0
                while True:
                    message = json.loads(await websocket.recv())

                    # full state update
                    if "panel" in message:
                        self._state.panel.panel_type = message["panel"]["panelType"]

                    if "zones" in message:
                        for id, zone in message["zones"].items():
                            self._state.zones[id] = Concord4Zone(zone)

                            if id in self._callbacks:
                                for callback in self._callbacks[id]:
                                    callback()

                    if "partitions" in message:
                        for id, partition in message["partitions"].items():
                            self._state.partitions[id] = Concord4Partition(partition)

                            if id in self._callbacks:
                                for callback in self._callbacks[id]:
                                    callback()

                    if "initialized" in message:
                        self._state.initialized = True

                    # single entity update
                    if "zone" in message:
                        self._state.zones[message["zone"]["id"]] = Concord4Zone(
                            message["zone"]
                        )
                        if message["zone"]["id"] in self._callbacks:
                            for callback in self._callbacks[message["zone"]["id"]]:
                                callback()

                    if "partition" in message:
                        self._state.partitions[
                            message["partition"]["id"]
                        ] = Concord4Partition(message["partition"])

                        if message["partition"]["id"] in self._callbacks:
                            for callback in self._callbacks[message["partition"]["id"]]:
                                callback()
            except:
                self._connected = False
                self._connect_attempt += 1

                if self._connect_attempt > 1:
                    await asyncio.sleep(15)

                continue

    async def connect(self) -> None:
        """Connect to Concord4WS."""
        self._loop.create_task(self._event_loop())

        while not self._state.initialized:
            await asyncio.sleep(0.1)

    async def disconnect(self) -> None:
        """Disconnect from Concord4WS."""
        self._loop.stop()
        self._loop.close()

        self._loop = asyncio.get_event_loop()

        self._connected = False

    def register_callback(
        self, zone_or_part_id: str, callback: Callable[[], None]
    ) -> None:
        """Register callback, called when zone or partition specified changes state."""
        self._callbacks.setdefault(zone_or_part_id, set()).add(callback)

    def remove_callback(
        self, zone_or_part_id: str, callback: Callable[[], None]
    ) -> None:
        """Remove previously registered callback."""
        self._callbacks[zone_or_part_id].remove(callback)
