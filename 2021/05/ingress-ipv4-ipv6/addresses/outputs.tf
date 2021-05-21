output "gke_ingress_ipv6_name" {
  value = google_compute_global_address.gke_ingress_ipv6.name
}

output "gke_ingress_ipv4_name" {
  value = google_compute_global_address.gke_ingress_ipv4.name
}
