import asyncio
import logging

import serfio

from . import network, wireguard

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TenMinuteVPN:
    def __init__(self):
        self.network = network.Network()
        self.serf = serfio.Serf()
        self.wg = wireguard.Wireguard(self.network, listen_port=51821)

    def create(self):
        self.wg.create()
        self.wg.configure()

    async def run(self):
        self.create()
        async with self.serf:
            members = await self.serf.members()
            logger.warning("members: %s", members)

            asyncio.create_task(self.subscribe())
            while True:
                await asyncio.sleep(60)

    async def subscribe(self):
        async for event in self.serf.stream():
            logger.warning("event: %s", event)
            if "Event" not in event:
                continue

            if event["Event"] == "member-join":
                for member in event["Members"]:
                    asyncio.create_task(self.query_member(member))

            if event["Event"] == "query":
                event_id = event["ID"]
                if event["Name"] == "tenminutevpn:endpoint":
                    payload = f"{self.network.IPV4_ADDRESS}:{self.wg.listen_port}"
                    self.publish(event_id, payload)

                if event["Name"] == "tenminutevpn:pubkey":
                    payload = self.wg.public_key
                    self.publish(event_id, payload)

                if event["Name"] == "tenminutevpn:address":
                    payload = self.network.PEER_ADDRESS
                    self.publish(event_id, payload)

    def publish(self, event_id, payload):
        coro = self.serf.respond(event_id, payload)
        asyncio.create_task(coro)

    async def query_member(self, member):
        node = member["Name"]

        endpoint = (
            await self.serf.query_one("tenminutevpn:endpoint", filter_nodes=[node])
        )["Payload"]

        pubkey = (
            await self.serf.query_one("tenminutevpn:pubkey", filter_nodes=[node])
        )["Payload"]

        address = (
            await self.serf.query_one("tenminutevpn:address", filter_nodes=[node])
        )["Payload"]

        if endpoint and pubkey and address:
            address = address.decode()
            endpoint_addr, endpoint_port = endpoint.decode().split(":")
            endpoint_port = int(endpoint_port)
            self.wg.add_peer(
                pubkey,
                [address],
                endpoint=(endpoint_addr, endpoint_port),
            )


def main():
    tmv = TenMinuteVPN()
    asyncio.run(tmv.run())


if __name__ == "__main__":
    main()
