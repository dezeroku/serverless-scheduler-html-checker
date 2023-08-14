terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.12"
    }
  }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
