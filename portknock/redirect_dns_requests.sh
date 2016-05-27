#!/bin/bash

echo nameserver 10.0.0.1 >> /etc/resolv.conf
echo "Nameserver added."

iptables -t nat -A PREROUTING -i enp0s8 -p udp --dport 53 -j DNAT --to-destination 10.0.2.15
echo "Added rule to redirect dns requests."
