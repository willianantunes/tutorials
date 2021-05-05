variable "network_name" {
  type = string
}

variable "instance_name" {
  description = "The desired name to assign to the deployed instance"
  default = "disk-instance-vm-test"
}

variable "image" {
  description = "The Docker image to deploy to GCE instances"
}

variable "env_variables" {
  type = map(string)
  default = null
}

variable "privileged_mode" {
  type = bool
  default = false
}

variable "activate_tty" {
  type = bool
  default = false
}

variable "custom_command" {
  type = list(string)
  default = null
}

variable "additional_metadata" {
  type = map(string)
  description = "Additional metadata to attach to the instance"
  default = null
}

variable "client_email" {
  description = "Service account email address"
  type = string
  default = null
}
