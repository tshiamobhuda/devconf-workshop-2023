##
# ChatGPT - Telegram Terraform Module
# AWS Lambda Resources
##

data "archive_file" "python_lambda_package" {  
  type = "zip"  
  source_file = "${path.module}/python/lambda_function.py" 
  output_path = "lambda.zip"
}

resource "aws_lambda_function" "chatgptt" {
        function_name = "chatgptt-lambda"
        filename      = "lambda.zip"
        source_code_hash = data.archive_file.python_lambda_package.output_base64sha256
        role          = aws_iam_role.lambda_role.arn
        runtime       = "python3.6"
        handler       = "lambda_function.lambda_handler"
        timeout       = 60
}
