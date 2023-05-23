##
# Contains reference across to the ChatGPT - Telegram Terraform Module
# Will output any information required from the deployment of the AWS resources.
##

output "lambda_name" {
  value       = aws_lambda_function.chatgpt.function_name
  description = "Created Lambda name"
}
