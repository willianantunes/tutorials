locals {
  tags = {
    terraform   = true
    environment = "prd"
    product     = "elastic-cloud"
  }
}

variable "kibana_endpoint" {}
variable "elasticsearch_endpoint" {}
variable "elasticsearch_service_account_name" {}
variable "elasticsearch_service_account_password" {
  type      = string
  sensitive = true
}
