resource "google_compute_managed_ssl_certificate" "jasmine_certs" {
  provider = google-beta

  name = "jasmine-certs"

  managed {
    domains = [
      "agrabah.com",
    ]
  }
}
