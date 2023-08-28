terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.14"
    }
  }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
