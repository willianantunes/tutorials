resource "google_compute_global_address" "gke_ingress_ipv6" {
  name = "external-address-gke-ingress-ipv6"
  ip_version = "IPV6"
  address_type = "EXTERNAL"
}

resource "google_compute_global_address" "gke_ingress_ipv4" {
  name = "external-address-gke-ingress-ipv4"
  ip_version = "IPV4"
  address_type = "EXTERNAL"
}
