output "profiles" {
  description = "User profile information"
  value       = aws_iam_user_login_profile.profiles
}

output "name" {
  description = "User name"
  value       = var.user.name
}

output "access_keys" {
  description = "User access keys information"
  value       = aws_iam_access_key.access_keys
}
