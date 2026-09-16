data "azurerm_client_config" "current" {}
resource "azurerm_key_vault" "main" {
  name = var.key_vault_name
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id = data.azurerm_client_config.current.tenant_id
  sku_name = "standard"
  soft_delete_retention_days = 7
  purge_protection_enabled = false
}
resource "azurerm_role_assignment" "terraform_kv" {
  scope = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id = data.azurerm_client_config.current.object_id
}
