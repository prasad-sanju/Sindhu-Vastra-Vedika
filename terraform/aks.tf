resource "azurerm_kubernetes_cluster" "main" {
  name = var.aks_name
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix = "svv-dev"
  default_node_pool { name = "system", vm_size = "Standard_D2s_v5", node_count = 1, vnet_subnet_id = azurerm_subnet.aks.id }
  identity { type = "SystemAssigned" }
  network_profile { network_plugin = "azure", load_balancer_sku = "standard" }
  oidc_issuer_enabled = true
  workload_identity_enabled = true
  key_vault_secrets_provider { secret_rotation_enabled = true }
}
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope = azurerm_container_registry.main.id
  role_definition_name = "AcrPull"
  principal_id = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}
