resource "aws_iam_user" "user" {
  name                 = var.user.name
  path                 = var.user.path
  tags                 = var.user.tags
  permissions_boundary = var.user.permissions_boundary
}

resource "aws_iam_user_policy_attachment" "managed_policies_attachments" {
  for_each = {
    for attached_policy in var.user.managed_policies : attached_policy.name => attached_policy
  }

  user       = var.user.name
  policy_arn = each.value.arn

  depends_on = [aws_iam_user.user]
}

resource "aws_iam_user_policy_attachment" "custom_policies_attachments" {
  for_each = {
    for attached_policy in var.user.custom_policies : attached_policy => attached_policy
  }

  user       = var.user.name
  policy_arn = var.policies[each.value].arn

  depends_on = [aws_iam_user.user]
}

resource "aws_iam_user_policy" "inline_policies" {
  for_each = {
    for inline_policy in var.user.inline_policies : inline_policy.name => inline_policy
  }

  name   = each.value.name
  user   = var.user.name
  policy = file(each.value.file_path)

  depends_on = [aws_iam_user.user]
}

resource "aws_iam_user_group_membership" "groups" {
  count = length(var.user.groups) > 0 ? 1 : 0

  user   = var.user.name
  groups = var.user.groups

  depends_on = [aws_iam_user.user]
}

resource "aws_iam_user_login_profile" "profiles" {
  count = var.user.need_password ? 1 : 0

  user    = var.user.name
  pgp_key = var.default_pgp_key

  lifecycle {
    ignore_changes = [
      password_length,
      password_reset_required,
      pgp_key,
    ]
  }

  depends_on = [aws_iam_user.user]
}

resource "aws_iam_access_key" "access_keys" {
  count = var.user.need_access_key ? 1 : 0

  user    = var.user.name
  pgp_key = var.default_pgp_key

  lifecycle {
    ignore_changes = [
      pgp_key,
    ]
  }

  depends_on = [aws_iam_user.user]
}
