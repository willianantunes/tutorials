locals {
  tags = {
    terraform   = true
    environment = "sandbox"
  }
}

resource "random_string" "arbitrary_id" {
  length  = 8
  numeric = false
  special = false
  upper   = false
}

resource "azurerm_resource_group" "sandbox_rg" {
  name     = "sandbox-${random_string.arbitrary_id.result}-rg"
  location = "westus2"
}

resource "azurerm_virtual_network" "hub" {
  name                = "hub-${random_string.arbitrary_id.result}-vnet"
  address_space       = ["10.10.0.0/16"]
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  tags                = local.tags
}

resource "azurerm_virtual_network" "spoke_site_a" {
  name                = "spoke-site-a-${random_string.arbitrary_id.result}-vnet"
  address_space       = ["10.11.0.0/16"]
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  tags                = local.tags
}

resource "azurerm_subnet" "spoke_site_a_subnet_blue" {
  name                 = "blue-${random_string.arbitrary_id.result}-sn"
  resource_group_name  = azurerm_resource_group.sandbox_rg.name
  virtual_network_name = azurerm_virtual_network.spoke_site_a.name
  address_prefixes     = ["10.11.0.0/21"]
}

resource "azurerm_subnet" "spoke_site_a_subnet_purple" {
  name                 = "purple-${random_string.arbitrary_id.result}-sn"
  resource_group_name  = azurerm_resource_group.sandbox_rg.name
  virtual_network_name = azurerm_virtual_network.spoke_site_a.name
  address_prefixes     = ["10.11.8.0/21"]
}

resource "azurerm_virtual_network" "spoke_site_b" {
  name                = "spoke-site-b-${random_string.arbitrary_id.result}-vnet"
  address_space       = ["10.12.0.0/16"]
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  tags                = local.tags
}
