module "lambda_handler" {
  providers = {
    aws = aws
  }

  # Hardcoded to point to a commit on the master branch
  source = "git::ssh://git@github.com/dezeroku/serverless-scheduler//terraform/src/modules/lambda_function?ref=6669e1f346db0dc600a1efb01316bf253a88b578"

  lambda_zip_path = var.lambda_zip_path
  function_name   = "${var.prefix}-html-checker"
  handler         = "serverless_scheduler_html_checker/handler.entrypoint"
  environment = {
    BUCKET_NAME   = aws_s3_bucket.state_bucket.id
    TEMPLATE_NAME = aws_ses_template.mail_template.name
    SOURCE_EMAIL  = var.source_email
  }
  additional_policy_arns = {
    bucket_access = aws_iam_policy.bucket_access.arn,
    ses_access    = aws_iam_policy.ses_access.arn
  }
  layer_arns = [
    var.common_layer_arn,
    var.plugins_layer_arn
  ]
  timeout = 15
}
