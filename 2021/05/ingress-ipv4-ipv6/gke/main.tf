######
###### GKE
# https://github.com/GoogleCloudPlatform/terraform-google-examples
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_cluster
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_node_pool

resource "google_container_cluster" "gke_cluster" {
  name = var.gke_name

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count = 1
}

resource "google_container_node_pool" "gke_cluster_node_pool" {
  name = "${var.gke_name}-default-node-pool"
  cluster = google_container_cluster.gke_cluster.name
  node_count = 1

  node_config {
    preemptible = true
    # https://cloud.google.com/sdk/gcloud/reference/container/clusters/create#--machine-type
    # gcloud compute machine-types list | grep standard | grep us-central1-a
    # n1-standard-1 / 1 / 3.75
    machine_type = "n1-standard-1"
    disk_size_gb = "10"
    # Type of the disk attached to each node (e.g. 'pd-standard', 'pd-balanced' or 'pd-ssd').
    # If unspecified, the default disk type is 'pd-standard'
    disk_type = "pd-ssd"
  }
}
