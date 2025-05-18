# Magalu cloud
variable "mgc_api_key" {
  type        = string
  description = "mgc api key"
}

variable "mgc_region" {
  type        = string
  description = "Magalu Cloud Region"
  default     = "br-ne1"
}

variable "ssh_key_path" {
  type        = string
  default     = "/home/augustodsgv/.ssh/mgc.pub"
  description = "path of public key in this computers"
}

variable "machine_image" {
  type        = string
  default     = "cloud-ubuntu-22.04 LTS"
  description = "virtual machine image"
}

variable "machine_type" {
  type        = string
  default     = "BV1-1-10"
  description = "VM flavor"
}

# Cloud flare
variable "cloudflare_api_token" {
  type        = string
  description = "cloud flare api token"
}

variable "cloudflare_zone_id" {
  type        = string
  description = "cloud flare zone id"
}