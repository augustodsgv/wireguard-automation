if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root"
   exit 1
fi

echo "Tearing down ufw and iptables..."

ufw route delete allow in on wg0 out on ens3
iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
ip6tables -t nat -D POSTROUTING -o ens3 -j MASQUERADE

ip link set down dev wg0
ip link del dev wg0

echo "Tear down finished"