# Virtual Machine
resource "mgc_ssh_keys" "wireguard_ssh_key" {
  provider = mgc
  key      = file(var.ssh_key_path)
  name     = "wireguard_ssh_key"
}

resource "mgc_virtual_machine_instances" "wireguard" {
  provider     = mgc
  name         = "wireguard"
  machine_type = var.machine_type
  image        = var.machine_image
  ssh_key_name = mgc_ssh_keys.wireguard_ssh_key.name
}

# Network
## VPC
resource "mgc_network_vpcs" "wireguard" {
  name        = "wireguard"
  description = "VPC for Wireguard VPN"
}

## Public IP
resource "mgc_network_public_ips" "wireguard" {
  provider    = mgc
  description = "http server public ip"
  vpc_id      = mgc_network_vpcs.wireguard.id
}

resource "mgc_network_public_ips_attach" "wireguard" {
  provider     = mgc
  public_ip_id = mgc_network_public_ips.wireguard.id
  interface_id = mgc_virtual_machine_instances.wireguard.network_interfaces[0].id
}

## Security Group
resource "mgc_network_security_groups" "wireguard_security_group" {
  provider = mgc
  name     = "wireguard_security_group"
}

resource "mgc_network_security_groups_rules" "wireguard_allow_ssh" {
  provider          = mgc
  direction         = "ingress"
  ethertype         = "IPv4"
  port_range_max    = 22
  port_range_min    = 22
  protocol          = "tcp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = mgc_network_security_groups.wireguard_security_group.id
}

resource "mgc_network_security_groups_rules" "wireguard_allow_vpn" {
  provider          = mgc
  direction         = "ingress"
  ethertype         = "IPv4"
  port_range_max    = 51820
  port_range_min    = 51820
  protocol          = "udp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = mgc_network_security_groups.wireguard_security_group.id
}

resource "mgc_network_security_groups_attach" "wireguard" {
  provider          = mgc
  security_group_id = mgc_network_security_groups.wireguard_security_group.id
  interface_id      = mgc_virtual_machine_instances.wireguard.network_interfaces[0].id
}