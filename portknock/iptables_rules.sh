#!/bin/bash

# IPTABLES
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
iptables -F
iptables -N KNOCKING
iptables -N GATE1
iptables -N PASSED

iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -j KNOCKING

# the recent module (called with -m recent), flags the requesting IP address with the name AUTH1
iptables -A GATE1 -p tcp --dport 1111 -m recent --name AUTH1 --set -j DROP

iptables -A GATE1 -m recent --name AUTH1 --remove
iptables -A GATE1 -p tcp --dport 2222 -m recent --name AUTH2 --set -j DROP

iptables -A GATE1 -m recent --name AUTH2 --remove
iptables -A GATE1 -p tcp --dport 3333 -m recent --name AUTH3 --set -j DROP

# drop all other packets
iptables -A GATE1 -j DROP

# open the SSH daemon for 30 seconds
iptables -A PASSED -m recent --name AUTH3 --remove

# accept SSH connections from the users who have made it into this chain
iptables -A PASSED -p tcp --dport 22 -j ACCEPT

# send all traffic that does not match back through to GATE1
iptables -A PASSED -j GATE1

# time limit to only give the successful client a 30 second window to connect to the daemon
iptables -A KNOCKING -m recent --rcheck --seconds 30 --name AUTH3 -j PASSED
# 10 second time limit before the previous knock expires also
iptables -A KNOCKING -m recent --rcheck --seconds 10 --name AUTH2 -j GATE1
iptables -A KNOCKING -m recent --rcheck --seconds 10 --name AUTH1 -j GATE1
iptables -A KNOCKING -j GATE1

#iptables -I PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-port 8000
#iptables -t nat -A POSTROUTING -j MASQUERADE