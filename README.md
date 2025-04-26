# About

DHCP Starvation Attack is a type of denial-of-service (DoS) attack that targets DHCP (Dynamic Host Configuration Protocol) servers. The goal of the attack is to exhaust the pool of available IP addresses that the DHCP server can assign to clients, preventing legitimate devices from obtaining an IP address and thus disrupting network connectivity.

# Dependencies
> Linux / Termux root
```
sudo apt install python3 python3-pip scapy -y
pip install scapy
```
# Install
```
git clone https://github.com/xiv3r/DHCP-Attack.git
cd DHCP-Attack
```
# Run
> for manual attack
```
python3 dhcpattack.py
```
> For basic attack
```
python3 dhcpbasic.py -i wlan0
```
> For starved.py
```
sudo python3 starved.py -i wlan0 -c 0 -d 0.5
```
