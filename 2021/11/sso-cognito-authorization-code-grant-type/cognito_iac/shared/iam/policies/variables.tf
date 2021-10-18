variable "policies" {
  description = "List of custom IAM policies"
  type = list(object({
    name        = string
    description = string
    path        = string
    file_path   = string
    vars        = map(string)
    tags        = map(string)
  }))

  default = []

  validation {
    condition = alltrue([
      for policy in var.policies : (
        length(policy.name) > 0 &&
        length(policy.path) > 0 &&
        length(policy.file_path) > 0
      )
    ])
    error_message = "All IAM custom policies must have a name, path and file_path!"
  }
}
