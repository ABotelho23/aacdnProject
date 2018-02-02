import logging
import socket
import sys
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf


def on_service_state_change(zeroconf, service_type, name, state_change):
    print("Service %s of type %s state changed: %s" % (name, service_type, state_change))

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            print("  Address: %s" % (socket.inet_ntoa(info.address)))
            print("  Port: %s" % (info.port,))
            print("  Hostname: %s" % (info.server,))
            if info.properties:
                print("  Properties are:")
                for key, value in info.properties.items():
                    print("    %s: %s" % (key, value))
            else:
                print("  No properties")
        else:
            print("  No info")
        print('\n')

def main():
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()
    print("\nBrowsing services...\n")
    browser = ServiceBrowser(zeroconf, "_coap._udp.local.", handlers=[on_service_state_change])

    sleep(5)
    print("\nEnding services browse...\n")
    zeroconf.close()
if __name__ == '__main__':
    main()
