##
# Contains reference across to the ChatGPT - Telegram Terraform Module
# Will output any information required from the deployment of the AWS resources.
##

output "lambda_name" {
  value       = module.chatgpt-telegram.lambda_name
  description = "Then name of the lambda"
}
