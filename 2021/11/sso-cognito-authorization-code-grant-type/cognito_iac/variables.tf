variable "groups" {
  default = []
}

variable "policies" {
  default = []
}

variable "users" {
  default = []
}

# https://gist.github.com/turingbirds/3df43f1920a98010667a
# https://devhints.io/gnupg
# https://stackoverflow.com/a/68780537/3899136
# You can generate your key, like:
# > gpg --generate-key && gpg --export | base64 > public.gpg
# Then you can create a file like `pgp_key.auto.tfvars` and provide the content of `public.gpg` as EOT to `pgp_key` variable!
variable "pgp_key" {
  type        = string
  description = "PGP Key used to encrypt IAM user secrets (like password and access secret key)"
}
