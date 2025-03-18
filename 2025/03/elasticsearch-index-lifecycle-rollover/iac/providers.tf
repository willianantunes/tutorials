terraform {
  required_providers {
    elasticstack = {
      source  = "elastic/elasticstack"
      version = "0.11.13"
    }
  }
}

provider "elasticstack" {
  kibana {
    username  = var.elasticsearch_service_account_name
    password  = var.elasticsearch_service_account_password
    endpoints = [var.kibana_endpoint]
  }
  elasticsearch {
    username  = var.elasticsearch_service_account_name
    password  = var.elasticsearch_service_account_password
    endpoints = [var.elasticsearch_endpoint]
  }
}
