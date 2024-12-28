# About

DHCP starvation attack which allocates a fake ips and mac to all subnet hosts until DHCP server cannot allocate ip to the clients.

# Dependencies
```
sudo apt install python3 python3-pip
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
python3 basicattack.py
```
