# Messing with wireguard
## What is VPN
VPN, or Virtual Private Network is a service that criptographs the clients internet packets and then
routes to a server (VPN server), that itself sends the packets to the destination.
It has three uses:
1. Make your access private: who really makes the requests is the server, so if you are using a public
VPN trackers can't know if it's you or other user using the VPN service. (So, keep in mind that if you are using
your own VPN it's not so private)
2. Make your access safe where internet access is not safe. Not all applications criptographs it's data before sending
to the server, so if a malicious person hacks into the network you are in (mind an airport or a hotel public networks), 
it can read all your private and compromissing data. The VPN will criptograph your data in your device (client) and only
the VPN server can uncriptograph it, so it will prevent that mans in the middle read your poodle photos.
3. Provide access to services or machines that are only in your local network. Once your private service or machine is reachable by your VPN server, it will be reachable by your client using the VPN. This is really useful once your service is not ready to be public but you need remote access to it or you have a vulnerable machine in your local network.
## How to configure Wireguard
### Pre configuring the server
To the wireguard service to run, you need to make a few network configurations in the server.

Firstly, you need to allow ipv4 traffic on your servers interfaces. To do so, enable it on `/etc/sysctl.conf` 
```diff
# vim /etc/sysctl.conf
# net.ipv4.ip_forward=1
+ net.ipv4.ip_forward=1
```
And enable it
```sh
sudo sysctl -p
```
Now, you need to configure the firewall. We will use ufw. First, download it
```sh
sudo apt install ufw -y
```
enable the wireguard and the ssh ports (if you are using).
```
sudo ufw allow 51820/udp
sudo ufw allow ssh
```
turn it on
```sh
sudo ufw enable
```
and last, but not least, download the wirguard
```sh
sudo apt install wireguard -y
```
### Generating the keys
Now, both you and the server need to make a pair of assimetric keys (a public and a private).
> The algorithm uses the public key to criptograph the message in a way that only who has the private key can uncriptograph it. So you can provide your public key to everyone, and who wants to make message readable only by you (or who has your private key) uses the public key to criptograph it.

To generate the keys, you can use the `wg genkey` and `wg pubkey` commands.
```sh
# Generating the private key
wg genkey > priv_key

# Generatingthe public key
wg pubkey < priv_key > pub_key
```
Do this for the server and for the client.

### Configuring the server
With the keys in hands, you can make the server file. It will look like this:
```conf
# /etc/wireguard/wg0.conf
PostUp = ufw route allow in on wg0 out on <server interface name>
PostUp = iptables -t nat -I POSTROUTING -o <server interface name> -j MASQUERADE
PostUp = ip6tables -t nat -I POSTROUTING -o <server interface name> -j MASQUERADE
PreDown = ufw route delete allow in on wg0 out on <server interface name>
PreDown = iptables -t nat -D POSTROUTING -o <server interface name> -j MASQUERADE
PreDown = ip6tables -t nat -D POSTROUTING -o <server interface name> -j MASQUERADE
SaveConfig = true

[Interface]
Address = <server private address>
ListenPort = 51820
PrivateKey = <server private key>

[Peer]
PublicKey = <client public key>
AllowedIPs = <client private address>
```

It's composede by three parts: network setup, interface(server) configs and peer (client) configs

First, the ```<server interface name>``` can be retrieved from the `ip command`.
```sh
# ip r s
...
default via 192.168.1.254 dev wlp0s20f3 proto dhcp metric 600
...
```
It's the one with `default`, in our case, it's the `wlp0s20f3`.

Next, you need to choose what private IP range you will use for your service. You can choose one of the `10.0.0.0/8`, `172.16.0.0/12` or `192.168.0.0/16`. Once decided, you can use the first of those IPs to be the `server private ip`. For example, if we choose the `10.0.0.0/8`, our IP is going to be `10.0.0.1/24`.

Both the <server private key> and the <client public key> were generated in the steps above, just place them here.

Finally, choose the `<client private address>`. It can be anyone within the defined private range. Let's choose `10.0.1.0/32`

Thus, our file will look like this
```conf
# /etc/wireguard/wg0.conf
PostUp = ufw route allow in on wg0 out on wlp0s20f3
PostUp = iptables -t nat -I POSTROUTING -o wlp0s20f3 -j MASQUERADE
PostUp = ip6tables -t nat -I POSTROUTING -o wlp0s20f3 -j MASQUERADE
PreDown = ufw route delete allow in on wg0 out on wlp0s20f3
PreDown = iptables -t nat -D POSTROUTING -o wlp0s20f3 -j MASQUERADE
PreDown = ip6tables -t nat -D POSTROUTING -o wlp0s20f3 -j MASQUERADE
SaveConfig = true

[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server private key>

[Peer]
PublicKey = <client public key>
AllowedIPs = 10.0.1.0
```

### Configuring the client
The client configuration is very similar, just a little bit more clean
```conf
# client_wg0.conf
[Interface]
Address = <client private address>
PrivateKey = <client private key>

[Peer]
PublicKey = <server public key>
AllowedIPs = <IPs to route to the VPN>
Endpoint = <VPN Server IP or domain name>:51820
```
The `<client private address>`, `<client private key>` and `<client private key>` were generate on the steps above, just place them here

The `<IPs to route to the VPN>` are the IPs that you want to be routen to the VPN. If you want to use the VPN only to access private services or machines, you can make only the route to tem go through the VPN. For example, imagine you have some machines in the same network of your VPN server with the 192.168.0.12 IP. You can make the VPN route only the 192.0.0.1/24.
If you want to make all traffic to go to the VPN, use the `0.0.0.0\0` cidr.

Last, but not least, place the VPN server public IP or domain name in the Endpoint config

## Running the service
### Server
Once all set, you can start the server VPN service using
```sh
sudo wg-quick up wg0
```
And all done, service running
### Linux client
If you are using a Linux client, download the wireguard and place the client configuration on `/etc/wireguard/wg0.conf` and use the same command
```sh
sudo wg-quick up wg0
```
### Android client
If you are using Android, you can simply download the wireguard app from app store and provide the generated file