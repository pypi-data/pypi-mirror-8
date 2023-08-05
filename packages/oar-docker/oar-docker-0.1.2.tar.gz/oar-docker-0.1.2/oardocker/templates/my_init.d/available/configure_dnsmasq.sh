#!/bin/sh
set -e

IP=$(ip -o -4 addr list eth0 | perl -n -e 'if (m{inet\s([\d\.]+)\/\d+\s}xms) { print $1 }')
echo "NAMESERVER_IP=$IP"

sed -i s/__LOCAL_IP__/$IP/ /etc/dnsmasq.conf

/etc/init.d/incron restart

