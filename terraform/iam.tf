resource "aws_iam_policy" "bucket_access" {
  policy = data.aws_iam_policy_document.bucket_access.json
}

data "aws_iam_policy_document" "bucket_access" {
  statement {
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      aws_s3_bucket.state_bucket.arn,
      "${aws_s3_bucket.state_bucket.arn}/*",
    ]
  }
}

resource "aws_iam_policy" "ses_access" {
  policy = data.aws_iam_policy_document.ses_access.json
}

data "aws_iam_policy_document" "ses_access" {
  statement {
    actions = [
      "ses:SendTemplatedEmail",
      "ses:SendEmail",
    ]
    resources = concat([
      data.aws_ses_domain_identity.mail_identity.arn,
      aws_ses_template.mail_template.arn,
    ], var.email_configuration_set != "" ? ["arn:aws:ses:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:configuration-set/${var.email_configuration_set}"] : [])
  }
}

data "aws_ses_domain_identity" "mail_identity" {
  domain = replace(var.source_email, "/.*@/", "")
}
