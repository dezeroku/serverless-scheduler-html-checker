# This config is meant to be used as an include in parent `serverless-checker`'s
# terraform/deployments/<DEPLOY_ENV>/plugins-serverless-scheduler-html-checker/terragrunt.hcl
# That's also where you should put proper `secret-values.tfvars`
terraform {
  source = "../../../..//plugins/serverless-scheduler-html-checker/terraform"

  extra_arguments "common_vars" {
    commands = get_terraform_commands_that_need_vars()
    required_var_files = [
      "${get_terragrunt_dir()}/../_secret_values/plugins-serverless-scheduler-html-checker-secret-values.tfvars",
    ]
  }
}

inputs = {
  aws_region                 = local.common_vars.locals.aws_region
  service                    = local.common_vars.locals.service
  stage                      = local.common_vars.locals.stage
  prefix                     = dependency.items_infra.outputs.prefix
  common_layer_arn           = dependency.common_lambda_layer.outputs.layer_arn
  plugins_layer_arn          = dependency.plugins_lambda_layer.outputs.layer_arn
  lambda_zip_path            = "${local.helper_vars.locals.deploy_dir}/plugins-serverless-scheduler-html-checker-lambda.zip"
  distribution_sns_topic_arn = dependency.distribution_sns.outputs.sns_topic_arn
}

dependency "items_infra" {
  config_path = "../items-infra"
}

dependency "common_lambda_layer" {
  config_path = "../common-lambda-layer-upload"
}

dependency "plugins_lambda_layer" {
  config_path = "../plugins-lambda-layer-upload"
}

dependency "distribution_sns" {
  config_path = "../distribution-sns"
}

locals {
  common_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  helper_vars = read_terragrunt_config(find_in_parent_folders("helpers_env.hcl"))
}
