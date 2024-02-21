output "vm_password" {
  value     = random_password.vm_admin_password.result
  sensitive = true
}
