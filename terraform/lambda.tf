locals {
    api_path      = "${path.module}/../api"
    api_dist_path = "${local.api_path}/dist"
  }
  
  data "external" "zip_hash" {
    program     = ["python3", "./hash.py", "./dist/api.zip"]
    working_dir = local.api_path
  }
  
  resource "aws_lambda_function" "get_comments_lambda" {
    filename         = "${local.api_dist_path}/api.zip"
    source_code_hash = data.external.zip_hash.result.hash
  
    role          = "ExampleRole"
    function_name = "get_comments_lambda"
    handler       = "main.handler"
    runtime       = "python3.8"
    timeout       = 60
    memory_size   = 128
    publish       = true
  
    tag = "GetCommentsLambda"
  }
  
  resource "aws_lambda_function_event_invoke_config" "get_comments_lambda" {
    function_name                = aws_lambda_function.get_comments_lambda.function_name
    maximum_event_age_in_seconds = 60
    maximum_retry_attempts       = 0
  }
  