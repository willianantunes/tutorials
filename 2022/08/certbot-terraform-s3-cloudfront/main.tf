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
# STUFF NEEDED SUCH AS LOCAL VARIABLES
# ---------------------------------------------------------------------------------------------------------------------

locals {
  dns = {
    zone = "amazonplayground.willianantunes.com"
  }
  s3 = {
    name             = "cockatielid-idp-dev-newuniversallogin"
    service_accounts = ["arn:aws:iam::YOUR_ACCOUNT_ID:user/cockatielid-dev-agrabah"]
  }
  cdn = {
    aliases = ["assets.amazonplayground.willianantunes.com"]
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# ACME certificate import
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_acm_certificate" "cert_assets_amazonplayground" {
  private_key       = file("${path.module}/etc-letsencrypt/live/assets.amazonplayground.willianantunes.com/privkey.pem")
  certificate_body  = file("${path.module}/etc-letsencrypt/live/assets.amazonplayground.willianantunes.com/cert.pem")
  certificate_chain = file("${path.module}/etc-letsencrypt/live/assets.amazonplayground.willianantunes.com/fullchain.pem")
}

# ---------------------------------------------------------------------------------------------------------------------
# S3 SETUP
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_s3_bucket" "origin" {
  bucket        = local.s3.name
  force_destroy = false

  tags = {
    Environemnt = "DEV/QA",
    Owner       = "Agrabah",
  }
}

resource "aws_s3_bucket_acl" "origin_bucket_acl" {
  bucket = aws_s3_bucket.origin.id
  acl    = "private"
}

resource "aws_s3_bucket_cors_configuration" "origin_bucket_cors" {
  bucket = aws_s3_bucket.origin.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = local.cdn.aliases
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
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

# ---------------------------------------------------------------------------------------------------------------------
# CDN SETUP
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_cloudfront_origin_access_identity" "oia_bucket_origin" {
  comment = "OAI for ${aws_s3_bucket.origin.bucket}"
}

resource "aws_cloudfront_distribution" "cdn" {
  comment             = "Cockatiel namespace managed by Terraform"
  default_root_object = "index.html"
  http_version        = "http2"
  # https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PriceClass.html
  price_class      = "PriceClass_All"
  enabled          = true
  is_ipv6_enabled  = true
  retain_on_delete = false
  tags = {
    "Environemnt" = "DEV/QA"
    "Name"        = "cockatielididp-dev-newuniversallogin"
    "Namespace"   = "cockatielididp"
    "Owner"       = "Agrabah"
    "Stage"       = "dev"
  }
  tags_all = {
    "Environemnt" = "DEV/QA"
    "Name"        = "cockatielididp-dev-newuniversallogin"
    "Namespace"   = "cockatielididp"
    "Owner"       = "Agrabah"
    "Stage"       = "dev"
  }
  wait_for_deployment = true
  default_cache_behavior {
    allowed_methods = [
      "DELETE",
      "GET",
      "HEAD",
      "OPTIONS",
      "PATCH",
      "POST",
      "PUT",
    ]
    cached_methods = [
      "GET",
      "HEAD",
    ]
    compress               = true
    default_ttl            = 60
    max_ttl                = 31536000
    min_ttl                = 0
    target_origin_id       = aws_s3_bucket.origin.bucket
    trusted_key_groups     = []
    trusted_signers        = []
    viewer_protocol_policy = "redirect-to-https"
    forwarded_values {
      headers = [
        "Access-Control-Request-Headers",
        "Access-Control-Request-Method",
        "Origin",
      ]
      query_string            = false
      query_string_cache_keys = []

      cookies {
        forward = "none"
      }
    }
  }

  origin {
    connection_attempts = 3
    connection_timeout  = 10
    origin_id           = aws_s3_bucket.origin.bucket
    domain_name         = aws_s3_bucket.origin.bucket_regional_domain_name

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oia_bucket_origin.cloudfront_access_identity_path
    }
  }

  aliases = local.cdn.aliases

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      # https://www.iso.org/obp/ui/#search
      locations = ["US", "BR", "PT"]
    }
  }

  viewer_certificate {
    acm_certificate_arn            = aws_acm_certificate.cert_assets_amazonplayground.arn
    cloudfront_default_certificate = true
    minimum_protocol_version       = "TLSv1"
    ssl_support_method             = "sni-only"
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# POLICIES
# ---------------------------------------------------------------------------------------------------------------------

# Policies regarding CDN

data "aws_iam_policy_document" "allow_cdn_read_s3" {
  statement {
    sid = "S3GetObjectForCloudFront"
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.origin.arn}/*",
    ]
    principals {
      identifiers = [aws_cloudfront_origin_access_identity.oia_bucket_origin.iam_arn]
      type        = "AWS"
    }
  }
  statement {
    sid = "S3ListBucketForCloudFront"
    actions = [
      "s3:ListBucket",
    ]
    resources = [
      aws_s3_bucket.origin.arn
    ]
    principals {
      identifiers = [aws_cloudfront_origin_access_identity.oia_bucket_origin.iam_arn]
      type        = "AWS"
    }
  }
}

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

# Policies regarding the service account

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

# Gathering everything in one single document

data "aws_iam_policy_document" "combined" {
  source_policy_documents = [
    data.aws_iam_policy_document.s3_ssl_only.json,
    data.aws_iam_policy_document.allow_cdn_read_s3.json,
    data.aws_iam_policy_document.s3_service_account_manager.json
  ]
}

resource "aws_s3_bucket_policy" "origin_bucket_policy_allow_cdn_read_s3" {
  bucket = aws_s3_bucket.origin.id
  policy = data.aws_iam_policy_document.combined.json
}

# ---------------------------------------------------------------------------------------------------------------------
# DNS entries
# ---------------------------------------------------------------------------------------------------------------------

data "aws_route53_zone" "selected_zone" {
  name = local.dns.zone
}

resource "aws_route53_record" "cdn_ipv4" {
  allow_overwrite = false
  name            = local.cdn.aliases[0]
  type            = "A"
  zone_id         = data.aws_route53_zone.selected_zone.zone_id
  alias {
    evaluate_target_health = false
    name                   = aws_cloudfront_distribution.cdn.domain_name
    zone_id                = aws_cloudfront_distribution.cdn.hosted_zone_id
  }
}

resource "aws_route53_record" "cdn_ipv6" {
  allow_overwrite = false
  name            = local.cdn.aliases[0]
  type            = "AAAA"
  zone_id         = data.aws_route53_zone.selected_zone.zone_id
  alias {
    evaluate_target_health = false
    name                   = aws_cloudfront_distribution.cdn.domain_name
    zone_id                = aws_cloudfront_distribution.cdn.hosted_zone_id
  }
}
