locals {
  # https://www.terraform.io/docs/language/values/locals.html
  instance_name = format("%s-%s", var.instance_name, substr(md5(module.gce-container.container.image), 0, 8))

  env_variables = [for var_name, var_value in var.env_variables : {
    name = var_name
    value = var_value
  }]
}

####################
##### CONTAINER SETUP

module "gce-container" {
  # https://github.com/terraform-google-modules/terraform-google-container-vm
  source = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"

  container = {
    image = var.image
    command = var.custom_command
    env = local.env_variables
    securityContext = {
      privileged : var.privileged_mode
    }
    tty : var.activate_tty
  }

  restart_policy = "Always"
}

####################
##### COMPUTE ENGINE

resource "google_compute_instance" "vm" {
  name = local.instance_name
  # gcloud compute machine-types list | grep micro | grep us-central1-a
  # e2-micro / 2 / 1.00
  # f1-micro / 1 / 0.60
  # gcloud compute machine-types list | grep small | grep us-central1-a
  # e2-small / 2 / 2.00
  # g1-small / 1 / 1.70
  machine_type = "f1-micro"
  # If true, allows Terraform to stop the instance to update its properties.
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = module.gce-container.source_image
    }
  }

  network_interface {
    network = var.network_name

    access_config {}
  }

  metadata = {
    gce-container-declaration = module.gce-container.metadata_value
  }

  labels = {
    container-vm = module.gce-container.vm_container_label
  }

  service_account {
    email = var.client_email
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
