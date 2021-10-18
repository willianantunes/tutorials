resource "aws_iam_policy" "policies" {
  for_each = { for policy in var.policies : policy.name => policy }

  name        = each.value.name
  description = each.value.description
  path        = each.value.path
  policy = (
    length(keys(each.value.vars)) > 0 ?
    templatefile(each.value.file_path, each.value.vars) :
    file(each.value.file_path)
  )
  tags = each.value.tags
}
