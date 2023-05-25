##
# Contains reference across to the ChatGPT - Telegram Terraform Module
# Declares any of the required inputs for the deployment.
##

variable "function_name" {
  type        = string
  description = "The name of the lambda function."
}
