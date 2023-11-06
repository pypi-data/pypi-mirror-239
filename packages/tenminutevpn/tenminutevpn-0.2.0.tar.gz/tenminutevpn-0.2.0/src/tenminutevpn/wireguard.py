import os

import pyroute2


class Wireguard:
    def __init__(self, network, private_key=None, listen_port=51820):
        self.network = network
        self.private_key = private_key or self.generate_private_key()
        self.public_key = self.generate_public_key(self.private_key)
        self.listen_port = listen_port

    @classmethod
    def generate_private_key(self):
        return os.popen("wg genkey").read().strip()

    @classmethod
    def generate_public_key(self, private_key):
        return os.popen(f"echo {private_key} | wg pubkey").read().strip()

    def create(self):
        with pyroute2.NDB() as ndb:
            if ndb.interfaces.exists(self.network.IFNAME):
                return

            with ndb.interfaces.create(
                kind="wireguard", ifname=self.network.IFNAME
            ) as link:
                link.add_ip(self.network.IPV4_NETWORK)
                link.add_ip(self.network.IPV6_NETWORK)
                link.set(state="up")

    def configure(self):
        with pyroute2.NDB() as ndb:
            with ndb.interfaces[self.network.IFNAME] as link:
                mtu = self.network.default_interface["mtu"] - 80
                if link.get("mtu") != mtu:
                    link.set("mtu", mtu)

        with pyroute2.WireGuard() as wg:
            wg.set(
                self.network.IFNAME,
                private_key=self.private_key,
                listen_port=self.listen_port,
            )

    def add_peer(self, public_key, allowed_ips, endpoint=None):
        peer = {
            "public_key": public_key,
            "allowed_ips": allowed_ips,
            "persistent_keepalive": 25,
        }

        if endpoint:
            endpoint_addr, endpoint_port = endpoint
            peer["endpoint_addr"] = endpoint_addr
            peer["endpoint_port"] = endpoint_port

        with pyroute2.WireGuard() as wg:
            wg.set(self.network.IFNAME, peer=peer)
