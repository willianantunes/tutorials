terraform {
  required_providers {
    elasticstack = {
      source  = "elastic/elasticstack"
      version = "0.11.15"
    }
  }
}

provider "elasticstack" {
  kibana {
    username  = var.elasticsearch_service_account_name
    password  = var.elasticsearch_service_account_password
    endpoints = [var.kibana_endpoint]
    insecure = true
  }
  elasticsearch {
    username  = var.elasticsearch_service_account_name
    password  = var.elasticsearch_service_account_password
    endpoints = [var.elasticsearch_endpoint]
    insecure = true
  }
}
