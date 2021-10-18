variable "groups" {
  description = "List of IAM groups"
  type = list(object({
    name            = string
    path            = string
    custom_policies = list(string) # List of custom attached policies names
    inline_policies = list(object({
      name      = string
      file_path = string
    })) # List of file paths for inline policies
    managed_policies = list(object({
      arn  = string
      name = string
    })) # List of managed policies arn attached to the group
  }))

  default = []

  validation {
    condition = alltrue([
      for group in var.groups : (length(group.name) > 0 && length(group.path) > 0)
    ])
    error_message = "All IAM defined groups must have a name and path!"
  }
}

variable "policies" {
  description = "List of IAM custom policies"
}
