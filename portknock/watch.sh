#!/bin/bash

while true; do
	sudo iptables -nvL > watch_iptables.log
	sleep 1
done

