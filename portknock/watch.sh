#!/bin/bash

while true; do
	iptables -nvL > watch_iptables.log
	sleep 1
done

