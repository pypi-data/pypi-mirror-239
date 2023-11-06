import os
import socket

import pyroute2


class Network:
    IFNAME = "tenminutevpn0"
    IPV4_ADDRESS = os.environ.get("IPV4_ADDRESS")
    PEER_ADDRESS = os.environ.get("PEER_ADDRESS")
    IPV4_NETWORK = "10.64.0.1/24"
    IPV6_NETWORK = "fd00:64::1/64"

    @property
    def hostname(self):
        return socket.gethostname()

    @property
    def default_route(self):
        with pyroute2.NDB() as ndb:
            return ndb.routes["default"]["oif"]

    @property
    def default_interface(self):
        with pyroute2.NDB() as ndb:
            return ndb.interfaces[self.default_route]
