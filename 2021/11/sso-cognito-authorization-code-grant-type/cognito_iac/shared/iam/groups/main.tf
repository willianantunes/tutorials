locals {
  managed_attached_policies = flatten([
    for group in var.groups : [
      for managed_policy in group.managed_policies : {
        group_name  = group.name
        policy_arn  = managed_policy.arn
        policy_name = managed_policy.name
      }
    ]
  ])

  custom_attached_policies = flatten([
    for group in var.groups : [
      for custom_policy in group.custom_policies : {
        group_name  = group.name
        policy_name = custom_policy
      }
    ]
  ])

  inline_policies = flatten([
    for group in var.groups : [
      for inline_policy in group.inline_policies : {
        group_name  = group.name
        policy_name = inline_policy.name
        file_path   = inline_policy.file_path
      }
    ]
  ])
}

resource "aws_iam_group" "groups" {
  for_each = { for group in var.groups : group.name => group }

  name = each.value.name
  path = each.value.path
}

resource "aws_iam_group_policy_attachment" "managed_policies_attachments" {
  for_each = {
    for attached_policy in local.managed_attached_policies :
    "${attached_policy.group_name}-${attached_policy.policy_name}" => attached_policy
  }

  group      = each.value.group_name
  policy_arn = each.value.policy_arn

  depends_on = [aws_iam_group.groups]
}

resource "aws_iam_group_policy_attachment" "custom_policies_attachments" {
  for_each = {
    for attached_policy in local.custom_attached_policies :
    "${attached_policy.group_name}-${attached_policy.policy_name}" => attached_policy
  }

  group      = each.value.group_name
  policy_arn = var.policies[each.value.policy_name].arn

  depends_on = [aws_iam_group.groups]
}

resource "aws_iam_group_policy" "inline_policies" {
  for_each = {
    for inline_policy in local.inline_policies :
    "${inline_policy.group_name}-${inline_policy.policy_name}" => inline_policy
  }

  name   = each.value.policy_name
  group  = each.value.group_name
  policy = file(each.value.file_path)
}
