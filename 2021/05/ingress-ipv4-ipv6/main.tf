######
###### CLOUD PROVIDERS

provider "google" {
  project = var.project
  credentials = file(var.credentials_file)
  region = var.region
  zone = var.zone
}

provider "google-beta" {
  project = var.project
  credentials = file(var.credentials_file)
  region = var.region
  zone = var.zone
}

######
###### REQUIREMENTS GCP

# You must have a GKE cluster created previously. This is just an example 😉
module "gke-instance" {
  source = "./gke"

  gke_name = "my-test-cluster"
  # After you create your cluster, you can do:
  # - gcloud container clusters list
  # And then use the cluster name to set your context:
  # - gcloud container clusters get-credentials [CLUSTER_NAME]
  # Your can check it through the following commands:
  # - kubectl config current-context
  # - kubectl config get-contexts
  # - kubectl config delete-context gke_active-triode-274813_us-central1-a_all-stuff-prd-default-cluster
}

module "addresses" {
  source = "./addresses"
}

module "certificates" {
  source = "./certificates"
}

data "google_client_config" "provider" {}

######
###### ABSTRACT PROVIDERS

provider "kubernetes" {
  # https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/using_gke_with_terraform
  host = "https://${module.gke-instance.cluster_endpoint}"
  token = data.google_client_config.provider.access_token
  cluster_ca_certificate = base64decode(module.gke-instance.cluster_ca_certificate, )
}

######
###### REQUIREMENTS K8S

# "The K8S definitions" will only work if you have the referenced service and its deployment.
# You can configure the "agrabah-np-service" here 😀

######
###### K8S DEFINITIONS

resource "kubernetes_ingress" "sample_ingress" {
  metadata {
    name = "sample-ingress"
    namespace = "production"

    annotations = {
      "kubernetes.io/ingress.global-static-ip-name" = module.addresses.gke_ingress_ipv6_name
      # If you have only one cert manager:
      "ingress.gcp.kubernetes.io/pre-shared-cert" = module.certificates.jasmine_cert_manager_name
      # If you have more than one, let's say two:
      # "ingress.gcp.kubernetes.io/pre-shared-cert" = "${module.certificates.jasmine_cert_manager_name},${module.certificates.jafar_cert_manager_name}"
    }
  }

  spec {
    rule {
      # You must change to a domain that you own if you'd like to see this in action 👀
      host = "agrabah.com"
      http {
        path {
          backend {
            service_name = "agrabah-np-service"
            service_port = 8000
          }
        }
      }
    }
  }
}
