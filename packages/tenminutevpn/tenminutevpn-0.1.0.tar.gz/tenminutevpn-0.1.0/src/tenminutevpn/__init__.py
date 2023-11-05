import pyroute2  # noqa: F401


def main():
    with pyroute2.NDB() as ndb:
        iface = ndb.routes["default"]["oif"]
        iface = ndb.interfaces[iface]["ifname"]
    print(iface)


if __name__ == "__main__":
    main()
