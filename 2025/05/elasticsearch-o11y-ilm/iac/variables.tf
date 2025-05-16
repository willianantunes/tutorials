locals {
  tags = {
    terraform   = true
    environment = "dev"
    project     = "observability"
    purpose     = "platform-tooling"
  }
}

variable "kibana_endpoint" {}
variable "elasticsearch_endpoint" {}
variable "elasticsearch_service_account_name" {}
variable "elasticsearch_service_account_password" {
  type      = string
  sensitive = true
}
