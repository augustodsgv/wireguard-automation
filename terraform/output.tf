output "public_ip" {
  value = mgc_network_public_ips.wireguard.public_ip
}

resource "local_file" "ansible_inventory" {
  filename = "../ansible/inventory.yaml"
  content = templatefile("inventory.yaml.tmpl", {
    public_ip = mgc_network_public_ips.wireguard.public_ip
  })

}