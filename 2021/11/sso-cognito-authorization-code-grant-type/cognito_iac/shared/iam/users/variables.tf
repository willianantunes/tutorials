variable "user" {
  description = "IAM User settings"
  type = object({
    name                 = string
    path                 = string
    permissions_boundary = string
    tags                 = map(string)
    custom_policies      = list(string)
    managed_policies = list(object({
      name = string
      arn  = string
    }))
    inline_policies = list(object({
      name      = string
      file_path = string
    }))
    groups          = list(string)
    need_password   = bool
    need_access_key = bool
  })

  validation {
    condition     = length(var.user.name) > 0 && length(var.user.path) > 0
    error_message = "Any IAM user must have a name and path!"
  }
}


variable "policies" {}

variable "default_pgp_key" {
  description = "Default PGP key"
  type        = string
}
