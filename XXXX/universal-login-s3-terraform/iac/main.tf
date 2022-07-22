terraform {
  required_version = ">= 1.0.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  profile             = "default"
  region              = "us-east-1"
  allowed_account_ids = ["YOUR_ACCOUNT_ID"]
  access_key          = "YOUR_ACCESS_KEY"
  secret_key          = "YOUR_SECRET_KEY"
}

# ---------------------------------------------------------------------------------------------------------------------
# REQUIRED VARIABLES
# ---------------------------------------------------------------------------------------------------------------------

locals {
  tags = {
    Stage              = "dev"
    Product            = "Auth0"
    Purpose            = "Identity provider"
    IsTerraformManaged = "true"
  }
  s3 = {
    name             = "dev-auth0-idp-sandbox"
    service_accounts = ["arn:aws:iam::YOUR_ACCOUNT_ID:user/auth0-uploadfiles-s3-idp"]
    cors = {
      allowed_origins = [
        "https://your-auth0-tenant.us.auth0.com",
        "https://antunes.us.auth0.com",
      ]
    }
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# S3 SETUP
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_s3_bucket" "origin" {
  bucket        = local.s3.name
  force_destroy = false

  tags = local.tags
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.origin.id

  block_public_acls       = false
  ignore_public_acls      = false
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_acl" "origin_bucket_acl" {
  bucket = aws_s3_bucket.origin.id
  acl    = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "origin_bucket_encryption" {
  bucket = aws_s3_bucket.origin.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_ownership_controls" "origin_bucket_ownership_controls" {
  bucket = aws_s3_bucket.origin.id

  rule {
    object_ownership = "ObjectWriter"
  }
}

resource "aws_s3_bucket_cors_configuration" "origin_bucket_cors" {
  bucket = aws_s3_bucket.origin.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = local.s3.cors.allowed_origins
    expose_headers  = []
    max_age_seconds = 3600
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# POLICIES
# ---------------------------------------------------------------------------------------------------------------------

data "aws_iam_policy_document" "s3_ssl_only" {
  statement {
    sid = "ForceSSLOnlyAccess"
    actions = [
      "s3:*",
    ]
    effect = "Deny"
    resources = [
      aws_s3_bucket.origin.arn,
      "${aws_s3_bucket.origin.arn}/*"
    ]
    condition {
      test = "Bool"
      values = [
        "false",
      ]
      variable = "aws:SecureTransport"
    }
    principals {
      identifiers = [
        "*",
      ]
      type = "*"
    }
  }
}

data "aws_iam_policy_document" "s3_service_account_manager" {
  statement {
    sid = "S3ServiceAccountManager"
    actions = [
      "s3:PutObjectAcl",
      "s3:PutObject",
      "s3:ListBucketMultipartUploads",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:GetBucketLocation",
      "s3:DeleteObject",
      "s3:AbortMultipartUpload",
    ]
    resources = [
      aws_s3_bucket.origin.arn,
      "${aws_s3_bucket.origin.arn}/*",
    ]
    principals {
      identifiers = local.s3.service_accounts
      type        = "AWS"
    }
  }
}

data "aws_iam_policy_document" "combined" {
  source_policy_documents = [
    data.aws_iam_policy_document.s3_ssl_only.json,
    data.aws_iam_policy_document.s3_service_account_manager.json
  ]
}

resource "aws_s3_bucket_policy" "origin_bucket_policy_allow_cdn_read_s3" {
  bucket = aws_s3_bucket.origin.id
  policy = data.aws_iam_policy_document.combined.json
}
