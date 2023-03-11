variable "aws_region" {
  type = string
}

variable "service" {
  type = string
}

variable "stage" {
  type = string
}

variable "prefix" {
  type = string
}

variable "lambda_zip_path" {
  type = string
}

variable "distribution_sns_topic_arn" {
  type = string
}

variable "common_layer_arn" {
  type = string
}

variable "plugins_layer_arn" {
  type = string
}

# TODO: add a variable for optionally setting up SQS buffer

# this is set by an <env>-secret-values.tfvars file
variable "source_email" {
  type = string
}
