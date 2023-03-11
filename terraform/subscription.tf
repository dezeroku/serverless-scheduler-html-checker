resource "aws_sns_topic_subscription" "distribution_subscription" {
  topic_arn = var.distribution_sns_topic_arn
  protocol  = "lambda"
  endpoint  = module.lambda_handler.function_arn
  # Handle only the jobs of a proper type
  filter_policy = jsonencode(
    {
      job_type = ["html_monitor_job"]
    }
  )
  filter_policy_scope = "MessageBody"
}

resource "aws_lambda_permission" "allow_sns" {
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_handler.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = var.distribution_sns_topic_arn
}
