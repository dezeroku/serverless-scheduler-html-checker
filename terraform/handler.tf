module "lambda_handler" {
  providers = {
    aws = aws
  }

  source = "../../../terraform/modules/lambda_function"

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
