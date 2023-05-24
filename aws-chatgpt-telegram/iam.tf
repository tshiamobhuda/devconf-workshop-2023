# resource "aws_iam_role" "lambda_exec_role" {

# }

# data "aws_iam_policy_document" "lambda_policy_doc" {

# }

resource "aws_iam_policy" "lambda_iam_policy" {
  name   = "${var.function_name}-policy"
  policy = data.aws_iam_policy_document.lambda_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_iam_policy.arn
  role       = aws_iam_role.lambda_exec_role.name
}
