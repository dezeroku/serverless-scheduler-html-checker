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

# the values below are meant to be set by a secret-values.tfvars file
variable "source_email" {
  type = string
}

variable "email_configuration_set" {
  type        = string
  default     = ""
  description = "If provided, IAM permissions are given to Lambda runner to use it"
}
