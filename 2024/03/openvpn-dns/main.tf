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

// region VNET

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

resource "azurerm_subnet" "hub_dmz" {
  name                 = "hub-dmz-${random_string.arbitrary_id.result}-sn"
  resource_group_name  = azurerm_resource_group.sandbox_rg.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.10.0.0/24"]
}

resource "azurerm_virtual_network" "spoke_1" {
  name                = "spoke-1-${random_string.arbitrary_id.result}-vnet"
  address_space       = ["10.11.0.0/16"]
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  tags                = local.tags
}

resource "azurerm_subnet" "spoke_1_aks" {
  name                 = "spoke-1-aks-${random_string.arbitrary_id.result}-sn"
  resource_group_name  = azurerm_resource_group.sandbox_rg.name
  virtual_network_name = azurerm_virtual_network.spoke_1.name
  address_prefixes     = ["10.11.0.0/21"]

  # AKS deploys a private endpoint in this subnet (which uses an Azure Private Link).
  private_endpoint_network_policies_enabled = true
}

// endregion

// region Peering connections

resource "azurerm_virtual_network_peering" "hub_and_spoke_1_peering" {
  name                      = "hub-to-spoke-1-peering"
  resource_group_name       = azurerm_resource_group.sandbox_rg.name
  virtual_network_name      = azurerm_virtual_network.hub.name
  remote_virtual_network_id = azurerm_virtual_network.spoke_1.id
}

resource "azurerm_virtual_network_peering" "spoke_1_and_hub_peering" {
  name                      = "spoke-1-to-hub-peering"
  resource_group_name       = azurerm_resource_group.sandbox_rg.name
  virtual_network_name      = azurerm_virtual_network.spoke_1.name
  remote_virtual_network_id = azurerm_virtual_network.hub.id
}

// endregion

// region OpenVPN Community Edition

resource "random_password" "vm_admin_password" {
  length      = 16
  special     = false
  min_upper   = 1
  min_lower   = 1
  min_numeric = 1
  min_special = 1
}

resource "azurerm_public_ip" "openvpn" {
  name                = "openvpn-${random_string.arbitrary_id.result}-pip"
  tags                = local.tags
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
  zones               = [1]
}

resource "azurerm_network_interface" "openvpn" {
  name                = "openvpn-${random_string.arbitrary_id.result}-nic"
  tags                = local.tags
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  ip_configuration {
    name                          = "openvpn-${random_string.arbitrary_id.result}-ip-configuration"
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.hub_dmz.id
    public_ip_address_id          = azurerm_public_ip.openvpn.id
  }
}

resource "azurerm_linux_virtual_machine" "openvpn" {
  name                  = "openvpn-${random_string.arbitrary_id.result}-vm"
  tags                  = local.tags
  location              = azurerm_resource_group.sandbox_rg.location
  resource_group_name   = azurerm_resource_group.sandbox_rg.name
  size                  = "Standard_DS1_v2"
  network_interface_ids = [azurerm_network_interface.openvpn.id]

  computer_name                   = "openvpn-vm"
  admin_username                  = "openvpn"
  admin_password                  = random_password.vm_admin_password.result
  disable_password_authentication = false

  source_image_reference {
    # Find images through this link: https://learn.microsoft.com/en-us/azure/virtual-machines/linux/cli-ps-findimage
    # az vm image list --location westus2 --architecture x64 --publisher Canonical --offer UbuntuServer --all --output table
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "18.04.202401161"
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  boot_diagnostics {
    storage_account_uri = null
  }
}

resource "azurerm_virtual_machine_extension" "openvpn" {
  virtual_machine_id = azurerm_linux_virtual_machine.openvpn.id
  tags               = local.tags
  name               = "openvpn-essential-packages"
  # https://learn.microsoft.com/en-us/azure/virtual-machines/extensions/custom-script-linux#supported-linux-distributions
  publisher            = "Microsoft.Azure.Extensions"
  type                 = "CustomScript"
  type_handler_version = "2.0"

  protected_settings = <<SETTINGS
  {
    "script": "${base64encode(templatefile("openvpn.sh",
  {
    public_ip        = azurerm_public_ip.openvpn.ip_address,
    public_dns_or_ip = azurerm_public_ip.openvpn.ip_address,
    user             = azurerm_linux_virtual_machine.openvpn.admin_username
  }
))}"
  }
  SETTINGS
}

// endregion

// region Network Security Group

resource "azurerm_subnet_network_security_group_association" "hub_dmz" {
  subnet_id                 = azurerm_subnet.hub_dmz.id
  network_security_group_id = azurerm_network_security_group.hub_dmz.id
}

resource "azurerm_network_security_group" "hub_dmz" {
  name                = "${azurerm_subnet.hub_dmz.name}-nsg"
  tags                = local.tags
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name

  # priorities: the LOWER, the STRONGER -> any number from [100, 4096]
  # https://docs.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview#security-rules

  security_rule {
    name     = "custom-deny-all-inbound"
    priority = 4096

    source_port_range      = "*"
    destination_port_range = "*"

    protocol  = "*"
    direction = "Inbound"

    source_address_prefix      = "*"
    destination_address_prefix = "*"

    access = "Deny"
  }

  security_rule {
    name        = "openvpn-port-inbound"
    description = "Allow inbound UDP access to OpenVPN and unrestricted egress"
    priority    = 100

    source_port_range      = "*"
    destination_port_range = "1194"

    protocol  = "Udp"
    direction = "Inbound"

    source_address_prefix      = "*"
    destination_address_prefix = "*"

    access = "Allow"
  }
}

// endregion

// region AKS

resource "azurerm_kubernetes_cluster" "main" {
  name = "${random_string.arbitrary_id.result}-aks"
  # https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions?tabs=azure-cli#aks-kubernetes-release-calendar
  kubernetes_version        = "1.28.3"
  tags                      = local.tags
  location                  = azurerm_resource_group.sandbox_rg.location
  resource_group_name       = azurerm_resource_group.sandbox_rg.name
  dns_prefix                = "${random_string.arbitrary_id.result}-aks"
  automatic_channel_upgrade = "patch"
  private_cluster_enabled   = true
  private_dns_zone_id       = "System"
  sku_tier                  = "Standard"

  identity {
    type = "SystemAssigned"
  }

  local_account_disabled = false

  default_node_pool {
    name           = "default"
    node_count     = 1
    vm_size        = "Standard_D2_v2"
    vnet_subnet_id = azurerm_subnet.spoke_1_aks.id
    os_sku         = "Ubuntu"
    tags           = local.tags
  }

  network_profile {
    network_plugin = "azure"
  }

  lifecycle {
    ignore_changes = [
      http_application_routing_enabled,
      http_proxy_config[0].no_proxy,
      kubernetes_version,
      default_node_pool[0].upgrade_settings
    ]
  }
}

resource "azurerm_private_dns_zone_virtual_network_link" "main_aks_hub" {
  name                  = "${azurerm_kubernetes_cluster.main.name}-${azurerm_virtual_network.hub.name}"
  tags                  = local.tags
  resource_group_name   = azurerm_kubernetes_cluster.main.node_resource_group
  private_dns_zone_name = regex("\\.(.+)", azurerm_kubernetes_cluster.main.private_fqdn)[0]
  virtual_network_id    = azurerm_virtual_network.hub.id
  registration_enabled  = false
}

// endregion
