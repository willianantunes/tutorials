locals {
  tags = {
    terraform   = true
    environment = "sandbox"
  }
  networks = {
    hub = {
      name = "hub"
      host = "hub-host-1"
    }
    spoke_site_a = {
      name = "spoke-site-a"
      host = "spoke-site-a-host-1"
    }
    spoke_site_b = {
      name = "spoke-site-b"
      host = "spoke-site-b-host-1"
    }
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

resource "azurerm_subnet" "hub_subnet_main" {
  name                 = "hub-main-${random_string.arbitrary_id.result}-sn"
  resource_group_name  = azurerm_resource_group.sandbox_rg.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.10.0.0/24"]
}

resource "azurerm_subnet" "hub_subnet_azure_firewall" {
  name                 = "AzureFirewallSubnet"
  resource_group_name  = azurerm_resource_group.sandbox_rg.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.10.1.0/24"]
}

resource "azurerm_virtual_network" "spoke_site_a" {
  name                = "spoke-site-a-${random_string.arbitrary_id.result}-vnet"
  address_space       = ["10.11.0.0/16"]
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  tags                = local.tags
}

resource "azurerm_subnet" "spoke_site_a_subnet_blue" {
  name                 = "spoke-site-a-blue-${random_string.arbitrary_id.result}-sn"
  resource_group_name  = azurerm_resource_group.sandbox_rg.name
  virtual_network_name = azurerm_virtual_network.spoke_site_a.name
  address_prefixes     = ["10.11.0.0/21"]
}

resource "azurerm_subnet" "spoke_site_a_subnet_purple" {
  name                 = "spoke-site-a-purple-${random_string.arbitrary_id.result}-sn"
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

resource "azurerm_subnet" "spoke_site_b_subnet_main" {
  name                 = "spoke-site-b-main-${random_string.arbitrary_id.result}-sn"
  resource_group_name  = azurerm_resource_group.sandbox_rg.name
  virtual_network_name = azurerm_virtual_network.spoke_site_b.name
  address_prefixes     = [azurerm_virtual_network.spoke_site_b.address_space[0]]
}

// endregion

// region Routing table

resource "azurerm_subnet_route_table_association" "hub" {
  subnet_id      = azurerm_subnet.hub_subnet_main.id
  route_table_id = azurerm_route_table.hub.id
}

resource "azurerm_route_table" "hub" {
  name                          = "hub-${random_string.arbitrary_id.result}-route-table"
  tags                          = local.tags
  location                      = azurerm_resource_group.sandbox_rg.location
  resource_group_name           = azurerm_resource_group.sandbox_rg.name
  disable_bgp_route_propagation = true

  route {
    name                   = "default-route"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = azurerm_firewall.hub.ip_configuration[0].private_ip_address
  }
}

resource "azurerm_subnet_route_table_association" "spoke_site_a_blue" {
  subnet_id      = azurerm_subnet.spoke_site_a_subnet_blue.id
  route_table_id = azurerm_route_table.spoke_site_a.id
}

resource "azurerm_subnet_route_table_association" "spoke_site_a_purple" {
  subnet_id      = azurerm_subnet.spoke_site_a_subnet_purple.id
  route_table_id = azurerm_route_table.spoke_site_a.id
}

resource "azurerm_route_table" "spoke_site_a" {
  name                          = "spoke-site-a-${random_string.arbitrary_id.result}-route-table"
  tags                          = local.tags
  location                      = azurerm_resource_group.sandbox_rg.location
  resource_group_name           = azurerm_resource_group.sandbox_rg.name
  disable_bgp_route_propagation = true

  route {
    name                   = "to-spoke-site-b"
    address_prefix         = azurerm_virtual_network.spoke_site_b.address_space[0]
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = azurerm_firewall.hub.ip_configuration[0].private_ip_address
  }

  route {
    name                   = "default-route"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = azurerm_firewall.hub.ip_configuration[0].private_ip_address
  }
}

resource "azurerm_subnet_route_table_association" "spoke_site_b" {
  subnet_id      = azurerm_subnet.spoke_site_b_subnet_main.id
  route_table_id = azurerm_route_table.spoke_site_b.id
}

resource "azurerm_route_table" "spoke_site_b" {
  name                          = "spoke-site-b-${random_string.arbitrary_id.result}-route-table"
  tags                          = local.tags
  location                      = azurerm_resource_group.sandbox_rg.location
  resource_group_name           = azurerm_resource_group.sandbox_rg.name
  disable_bgp_route_propagation = true

  route {
    name                   = "to-spoke-site-a"
    address_prefix         = azurerm_virtual_network.spoke_site_a.address_space[0]
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = azurerm_firewall.hub.ip_configuration[0].private_ip_address
  }

  route {
    name                   = "default-route"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = azurerm_firewall.hub.ip_configuration[0].private_ip_address
  }
}

// endregion

// region Peering connections

resource "azurerm_virtual_network_peering" "hub_and_spoke_site_a_peering" {
  name                      = "${local.networks.hub.name}-to-${local.networks.spoke_site_a.name}-peering"
  resource_group_name       = azurerm_resource_group.sandbox_rg.name
  virtual_network_name      = azurerm_virtual_network.hub.name
  remote_virtual_network_id = azurerm_virtual_network.spoke_site_a.id
  allow_forwarded_traffic   = true
}

resource "azurerm_virtual_network_peering" "spoke_site_a_and_hub_peering" {
  name                      = "${local.networks.spoke_site_a.name}-to-${local.networks.hub.name}-peering"
  resource_group_name       = azurerm_resource_group.sandbox_rg.name
  virtual_network_name      = azurerm_virtual_network.spoke_site_a.name
  remote_virtual_network_id = azurerm_virtual_network.hub.id
  allow_forwarded_traffic   = true
}

resource "azurerm_virtual_network_peering" "hub_and_spoke_site_b_peering" {
  name                      = "${local.networks.hub.name}-to-${local.networks.spoke_site_b.name}-peering"
  resource_group_name       = azurerm_resource_group.sandbox_rg.name
  virtual_network_name      = azurerm_virtual_network.hub.name
  remote_virtual_network_id = azurerm_virtual_network.spoke_site_b.id
  allow_forwarded_traffic   = true
}

resource "azurerm_virtual_network_peering" "spoke_site_b_and_hub_peering" {
  name                      = "${local.networks.spoke_site_b.name}-to-${local.networks.hub.name}-peering"
  resource_group_name       = azurerm_resource_group.sandbox_rg.name
  virtual_network_name      = azurerm_virtual_network.spoke_site_b.name
  remote_virtual_network_id = azurerm_virtual_network.hub.id
  allow_forwarded_traffic   = true
}

// endregion

// region Public IPs

resource "azurerm_public_ip" "azure_firewall" {
  name                = "firewall-${random_string.arbitrary_id.result}-pip"
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  tags                = local.tags
  allocation_method   = "Static"
  sku                 = "Standard"
}

// endregion

// region Azure Firewall

resource "azurerm_firewall" "hub" {
  name                = "hub-${random_string.arbitrary_id.result}-fw"
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  tags                = local.tags
  sku_name            = "AZFW_VNet"
  sku_tier            = "Standard"

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.hub_subnet_azure_firewall.id
    public_ip_address_id = azurerm_public_ip.azure_firewall.id
  }
}

resource "azurerm_firewall_network_rule_collection" "spoke-to-spoke-traffic" {
  name                = "spoke-to-spoke-traffic"
  azure_firewall_name = azurerm_firewall.hub.name
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  priority            = 100
  action              = "Allow"

  rule {
    # This enables ANY traffic from the spoke site A to the spoke site B
    # You don't need the rule "spoke-site-b-to-spoke-site-a" to make spoke site B to reply ICMP requests to spoke site A
    name = "spoke-site-a-to-spoke-site-b"

    source_addresses = [
      azurerm_virtual_network.spoke_site_a.address_space[0]
    ]

    destination_ports = [
      "*",
    ]

    destination_addresses = [
      azurerm_virtual_network.spoke_site_b.address_space[0]
    ]

    protocols = [
      "Any",
    ]
  }

  rule {
    name = "spoke-site-b-to-spoke-site-a"

    source_addresses = [
      azurerm_virtual_network.spoke_site_b.address_space[0]
    ]

    destination_ports = [
      "*",
    ]

    destination_addresses = [
      azurerm_virtual_network.spoke_site_a.address_space[0]
    ]

    protocols = [
      "Any",
    ]
  }
}

resource "azurerm_firewall_network_rule_collection" "internet-traffic" {
  name                = "internet-traffic"
  azure_firewall_name = azurerm_firewall.hub.name
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  priority            = 101
  action              = "Allow"

  rule {
    name = "hub-and-spoke-to-internet"

    source_addresses = [
      azurerm_virtual_network.spoke_site_a.address_space[0],
      azurerm_virtual_network.spoke_site_b.address_space[0],
      azurerm_virtual_network.hub.address_space[0],
    ]

    destination_ports = [
      "80",
      "443",
    ]

    destination_addresses = [
      "*"
    ]

    protocols = [
      "TCP",
    ]
  }
}

// endregion

// region NAT Gateway

resource "azurerm_public_ip" "nat_gateway_1" {
  name                = "nat-gateway-1-${random_string.arbitrary_id.result}-pip"
  tags                = local.tags
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
  zones               = [1]
}

resource "azurerm_nat_gateway" "main" {
  name                = "main-${random_string.arbitrary_id.result}-ng"
  tags                = local.tags
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  sku_name            = "Standard"
}

resource "azurerm_nat_gateway_public_ip_association" "main_1" {
  nat_gateway_id       = azurerm_nat_gateway.main.id
  public_ip_address_id = azurerm_public_ip.nat_gateway_1.id
}

resource "azurerm_subnet_nat_gateway_association" "main_hub_subnet_azure_firewall" {
  subnet_id      = azurerm_subnet.hub_subnet_azure_firewall.id
  nat_gateway_id = azurerm_nat_gateway.main.id
}

// endregion

// region Virtual machines

resource "random_password" "vm_admin_password" {
  length  = 16
  special = false
}

resource "azurerm_network_interface" "hub_host_1" {
  name                = "${local.networks.hub.host}-${random_string.arbitrary_id.result}-nic"
  tags                = local.tags
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  ip_configuration {
    name                          = "${local.networks.hub.host}-${random_string.arbitrary_id.result}-ip-configuration"
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.hub_subnet_main.id
  }
}

resource "azurerm_linux_virtual_machine" "hub_host_1" {
  name                  = "${local.networks.hub.host}-${random_string.arbitrary_id.result}-vm"
  tags                  = local.tags
  location              = azurerm_resource_group.sandbox_rg.location
  resource_group_name   = azurerm_resource_group.sandbox_rg.name
  size                  = "Standard_B2pts_v2"
  network_interface_ids = [azurerm_network_interface.hub_host_1.id]

  computer_name                   = "${local.networks.hub.host}-vm"
  admin_username                  = local.networks.hub.host
  admin_password                  = random_password.vm_admin_password.result
  disable_password_authentication = false

  source_image_reference {
    # Find images through this link: https://learn.microsoft.com/en-us/azure/virtual-machines/linux/cli-ps-findimage
    # az vm image list --location westus2 --publisher Canonical --offer 0001-com-ubuntu-server-jammy --all --output table
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-arm64"
    version   = "22.04.202206220"
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  boot_diagnostics {
    storage_account_uri = null
  }
}

resource "azurerm_network_interface" "spoke_site_a_host_1" {
  name                = "${local.networks.spoke_site_a.host}-${random_string.arbitrary_id.result}-nic"
  tags                = local.tags
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  ip_configuration {
    name                          = "${local.networks.spoke_site_a.host}-${random_string.arbitrary_id.result}-ip-configuration"
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.spoke_site_a_subnet_blue.id
  }
}

resource "azurerm_linux_virtual_machine" "spoke_site_a_host_1" {
  name                  = "${local.networks.spoke_site_a.host}-${random_string.arbitrary_id.result}-vm"
  tags                  = local.tags
  location              = azurerm_resource_group.sandbox_rg.location
  resource_group_name   = azurerm_resource_group.sandbox_rg.name
  size                  = "Standard_B2pts_v2"
  network_interface_ids = [azurerm_network_interface.spoke_site_a_host_1.id]

  computer_name                   = "${local.networks.spoke_site_a.host}-vm"
  admin_username                  = local.networks.spoke_site_a.host
  admin_password                  = random_password.vm_admin_password.result
  disable_password_authentication = false

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-arm64"
    version   = "22.04.202206220"
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  boot_diagnostics {
    storage_account_uri = null
  }
}

resource "azurerm_network_interface" "spoke_site_b_host_1" {
  name                = "${local.networks.spoke_site_b.host}-${random_string.arbitrary_id.result}-nic"
  tags                = local.tags
  location            = azurerm_resource_group.sandbox_rg.location
  resource_group_name = azurerm_resource_group.sandbox_rg.name
  ip_configuration {
    name                          = "${local.networks.spoke_site_b.host}-${random_string.arbitrary_id.result}-ip-configuration"
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.spoke_site_b_subnet_main.id
  }
}

resource "azurerm_linux_virtual_machine" "spoke_site_b_host_1" {
  name                  = "${local.networks.spoke_site_b.host}-${random_string.arbitrary_id.result}-vm"
  tags                  = local.tags
  location              = azurerm_resource_group.sandbox_rg.location
  resource_group_name   = azurerm_resource_group.sandbox_rg.name
  size                  = "Standard_B2pts_v2"
  network_interface_ids = [azurerm_network_interface.spoke_site_b_host_1.id]

  computer_name                   = "${local.networks.spoke_site_b.host}-vm"
  admin_username                  = local.networks.spoke_site_b.host
  admin_password                  = random_password.vm_admin_password.result
  disable_password_authentication = false

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-arm64"
    version   = "22.04.202206220"
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  boot_diagnostics {
    storage_account_uri = null
  }
}

// endregion
