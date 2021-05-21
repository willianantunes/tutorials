output "cluster_ca_certificate" {
  value = google_container_cluster.gke_cluster.master_auth[0].cluster_ca_certificate
}

output "cluster_endpoint" {
  value = google_container_cluster.gke_cluster.endpoint
}
