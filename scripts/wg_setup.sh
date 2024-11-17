if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
echo "Setting up ufw and iptables..."

ip link add dev wg0 type wireguard
ip address add dev wg0 10.0.0.1/24
wg setconf wg0 ./wg0.conf
ip link set up dev wg0

ufw route allow in on wg0 out on ens3
iptables -t nat -I POSTROUTING -o ens3 -j MASQUERADE
ip6tables -t nat -I POSTROUTING -o ens3 -j MASQUERADE
echo "Setup finished"