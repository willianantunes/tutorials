output "cognito_user_pool" {
  # terraform output -json cognito_user_pool | jq '.user_pool.id'
  description = "All outputs exposed by the module."
  value       = merge(module.cognito_user_pool, { client_secrets = null })
}

output "cognito_clients" {
  description = "All Cognito User Pool Client resources associated with the Cognito User Pool."
  value       = { for client in module.cognito_user_pool.clients : client.name => merge(client, { client_secret = null }) }
}

output "cognito_client_secrets" {
  description = "The secrets of all created Cognito User Pool Client resources."
  value       = module.cognito_user_pool.client_secrets
  sensitive   = true
}

output "iam_encrypted_secrets" {
  # To retrieve it: terraform output iam_encrypted_secrets
  description = "IAM Users encrypted secrets"
  value = {
    for iam_user in module.iam_users : iam_user.name => iam_user.profiles[0].encrypted_password
    if length(iam_user.profiles) > 0
  }
  sensitive = true
}

output "iam_encrypted_access_keys" {
  # To retrieve it: terraform output iam_encrypted_access_keys
  # Decrypting the secret: terraform output -json iam_encrypted_access_keys | jq '.["poc-cognito-custom-ui-api"].encrypted_secret' | sed 's/ //g' | sed 's/"//g' | base64 -d | gpg -d
  description = "IAM Users encrypted Access Keys"
  value = {
    for iam_user in module.iam_users : iam_user.name => {
      access_key       = iam_user.access_keys[0].id
      encrypted_secret = iam_user.access_keys[0].encrypted_secret
    }
    if length(iam_user.access_keys) > 0
  }
  sensitive = true
}
