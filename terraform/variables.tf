variable "location" {
  type    = string
  default = "Central India"
}

variable "resource_group_name" {
  type    = string
  default = "svv-dev-rg"
}

variable "vnet_name" {
  type    = string
  default = "svv-dev-vnet"
}

variable "aks_name" {
  type    = string
  default = "svv-dev-aks"
}

variable "acr_name" {
  type    = string
  default = "REPLACE_WITH_UNIQUE_ACR"
}

variable "key_vault_name" {
  type    = string
  default = "REPLACE_WITH_UNIQUE_KV"
}
