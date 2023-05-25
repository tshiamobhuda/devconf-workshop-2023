##
# ChatGPT - Telegram Terraform Module
# AWS Lambda Resources
##

data "archive_file" "dummy" {
  type        = "zip"
  output_path = "${path.module}/lambda_dummy_package.zip"
  source {
    content  = "hello"
    filename = "dummy.text"
  }
}

resource "aws_lambda_function" "chatgpt" {
  function_name                  = var.function_name
  filename                       = data.archive_file.dummy.output_path
  description                    = "Process interaction between ChatGPT and Telegram."
  handler                        = "lambda_function.message_handler"
  runtime                        = "python3.10"
  reserved_concurrent_executions = 5
  role                           = aws_iam_role.lambda_exec_role.arn
  memory_size                    = 128
  timeout                        = 300
}

resource "aws_lambda_function_url" "chatgpt" {
  function_name      = aws_lambda_function.chatgpt.function_name
  authorization_type = "NONE"
}
