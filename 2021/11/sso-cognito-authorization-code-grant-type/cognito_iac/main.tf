terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.60"
    }
  }

  required_version = ">= 1.0.7"
}

provider "aws" {
  profile             = "default"
  region              = "us-east-1"
  allowed_account_ids = ["YOUR-ACCOUNT-ID"]
}

# ---------------------------------------------------------------------------------------------------------------------
# STUFF NEEDED SUCH AS LOCAL VARIABLES
# ---------------------------------------------------------------------------------------------------------------------

locals {
  users = [
    {
      name                 = "poc-cognito-custom-ui-api"
      path                 = "/"
      permissions_boundary = ""
      managed_policies = [
        {
          arn  = "arn:aws:iam::aws:policy/AmazonCognitoPowerUser"
          name = "AmazonCognitoPowerUser"
        },
      ]
      custom_policies = []
      inline_policies = []
      groups = [
        "service-accounts",
      ]
      tags            = {}
      need_password   = false
      need_access_key = true
    },
  ]
}

# ---------------------------------------------------------------------------------------------------------------------
# IAM
# ---------------------------------------------------------------------------------------------------------------------

module "iam_policies" {
  source = "./shared/iam/policies"

  policies = []
}

module "iam_groups" {
  source = "./shared/iam/groups"

  groups = [
    {
      name             = "service-accounts"
      path             = "/"
      managed_policies = []
      custom_policies  = []
      inline_policies  = []
    },
  ]
  policies = module.iam_policies.policies

  depends_on = [module.iam_policies]
}

module "iam_users" {
  source = "./shared/iam/users"

  for_each        = { for user in local.users : user.name => user }
  user            = each.value
  policies        = module.iam_policies.policies
  default_pgp_key = var.pgp_key

  depends_on = [module.iam_policies, module.iam_groups]
}

# ---------------------------------------------------------------------------------------------------------------------
# COGNITO USER POOL
# ---------------------------------------------------------------------------------------------------------------------

# Know more at: https://github.com/mineiros-io/terraform-aws-cognito-user-pool/blob/0ba192ca3af987887da092ee268af0981924dbae/examples/complete/main.tf
module "cognito_user_pool" {
  source  = "mineiros-io/cognito-user-pool/aws"
  version = "0.7.0"

  name = "poc-users-cognito-tmp"

  # Set to False if users can sign themselves up via an app
  allow_admin_create_user_only = false

  enable_username_case_sensitivity = false
  advanced_security_mode           = "OFF"

  username_attributes = [
    "email",
  ]

  account_recovery_mechanisms = [
    {
      name     = "verified_email"
      priority = 1
    },
    {
      name     = "verified_phone_number"
      priority = 2
    }
  ]

  # If invited by an admin
  invite_email_subject = "You've been invited to Agrabah"
  invite_email_message = "Hi {username}, your temporary password is '{####}'."
  invite_sms_message   = "Hi {username}, your temporary password is '{####}'."

  domain                = "situation-auth-playground"
  default_email_option  = "CONFIRM_WITH_LINK"
  email_subject_by_link = "Your Verification Link"
  email_message_by_link = "Please click the link below to verify your email address. {##Verify Email##}."
  sms_message           = "Your verification code is {####}."

  challenge_required_on_new_device = true
  user_device_tracking             = "USER_OPT_IN"

  # Require MFA
  mfa_configuration        = "OPTIONAL"
  allow_software_mfa_token = true

  password_minimum_length    = 8
  password_require_lowercase = false
  password_require_numbers   = false
  password_require_uppercase = false
  password_require_symbols   = false

  temporary_password_validity_days = 3

  # https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html
  # https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases
  # Developers can use the preferred_username attribute to give users a username that they can change. For more information, see Overview of Aliases.
  schema_attributes = [
    {
      # overwrites the default attribute 'email'
      name       = "email",
      type       = "String"
      required   = true
      min_length = 5
      max_length = 320
    },
    {
      # overwrites the default attribute 'name'
      name       = "name",
      type       = "String"
      required   = false
      min_length = 3
      max_length = 70
    }
  ]

  clients = [
    {
      name                                 = "poc-product_a-appclientcognito-tmp"
      supported_identity_providers         = ["COGNITO"]
      read_attributes                      = ["name", "email", "email_verified", "preferred_username"]
      allowed_oauth_scopes                 = ["email", "openid", "profile"]
      allowed_oauth_flows                  = ["code"]
      logout_urls                          = ["http://localhost:8000/logout"]
      callback_urls                        = ["http://localhost:8000/api/v1/response-oidc"]
      default_redirect_uri                 = "http://localhost:8000/api/v1/response-oidc"
      allowed_oauth_flows_user_pool_client = true
      generate_secret                      = true
    },
    {
      name                                 = "poc-product_b-appclientcognito-tmp"
      supported_identity_providers         = ["COGNITO"]
      read_attributes                      = ["name", "email", "email_verified", "preferred_username"]
      allowed_oauth_scopes                 = ["email", "openid", "profile"]
      allowed_oauth_flows                  = ["code"]
      logout_urls                          = ["http://localhost:8001/logout"]
      callback_urls                        = ["http://localhost:8001/api/v1/response-oidc"]
      default_redirect_uri                 = "http://localhost:8001/api/v1/response-oidc"
      allowed_oauth_flows_user_pool_client = true
      generate_secret                      = true
    }
  ]

  tags = {
    environment = "poc"
  }
}
