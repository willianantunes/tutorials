provider "google" {
  project = var.project
  credentials = file(var.credentials_file)
  region = var.region
  zone = var.zone
}

module "gce-worker-container" {
  source = "./gce-with-container"

  image = "gcr.io/${var.project}/jafar@sha256:6b71cebad455dae81af9fcb87a4c8b5bca2c2b6b2c09cec21756acd0f1ae7cec"
  privileged_mode = true
  activate_tty = true
  custom_command = [
    "./scripts/start-worker.sh"
  ]
  env_variables = {
    Q_CLUSTER_WORKERS = "2"
    DB_HOST = "your-database-host"
    DB_PORT = "5432"
    DB_ENGINE = "django.db.backends.postgresql"
    DB_NAME = "db_production"
    DB_SCHEMA = "jafar_prd"
    DB_USER = "role_jafar_prd"
    DB_PASS = "this-is-my-honest-password"
    DB_USE_SSL = "True"
  }
  instance_name = "jafar-worker"
  network_name = "default"
  # This has the permission to download images from Container Registry
  client_email = "custom-gce-dealer@${var.project}.iam.gserviceaccount.com"
}
