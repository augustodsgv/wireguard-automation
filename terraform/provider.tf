terraform {
  required_providers {
    mgc = {
      source  = "MagaluCloud/mgc"
      version = "0.33.0"
    }

    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5"
    }
  }
}

# Magalu cloud provider
provider "mgc" {
  region  = var.mgc_region
  api_key = var.mgc_api_key
}

# Cloud flare provider
# provider "cloudflare" {
#   api_token = var.cloudflare_api_token

# }