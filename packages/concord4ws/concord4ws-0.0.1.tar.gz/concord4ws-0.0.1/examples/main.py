import asyncio
from concord4ws import Concord4WSClient


async def main():
    client = Concord4WSClient("127.0.0.01", 8080)

    if await client.test_connect():
        print("Connected")
    else:
        print("Not Connected")

    zoneCallback = lambda: print(client._state.zones)
    partitionCallback = lambda: print(client._state.partitions)

    await client.connect()

    print("Ready!")

    for zone in client._state.zones:
        client.register_callback(zone, zoneCallback)

    for partition in client._state.partitions:
        client.register_callback(partition, partitionCallback)

    await asyncio.futures.Future()


asyncio.run(main())
