resource "azurerm_resource_group" "main" {
  name = var.resource_group_name
  location = var.location
  tags = { project = "Sindhu Vastra Vedika", environment = "dev", managed_by = "terraform" }
}
